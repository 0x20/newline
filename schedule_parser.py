#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
"""
Schedule parser to convert json schedule to pentabarf XML

This parser reads the Newline schedule in JSON format and produces a valid
Pentabarf XML file. This XML is used by the Giggity Android app to navigate
Newline schedule.

Copyright (C) 2018 Dieter Adriaenssens <ruleant@users.sourceforge.net>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from os.path import isfile
from datetime import date, datetime, timedelta
import time
import json
from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Room import Room
from pentabarf.Event import Event

def main():
    """ Main function, reads the json file and generates the Pentabarf XML """

    current_year = datetime.now().strftime("%Y")

    json_input_file = '%s/json/data.json' % (current_year)
    pentabarf_file = '%s/xml/pentabarf.xml' % (current_year)

    try:
        conference = read_json(json_input_file)
    except IOError as exc:
        print 'IOError : %s' % str(exc.message)
        exit()

    generate_pentabarf_xml(conference, pentabarf_file)

def read_json(json_input_file):
    """ Read and parse the conference schedule JSON file """

    if not isfile(json_input_file):
        raise IOError("Inputfile '%s' does not exist" % json_input_file)

    conferenceName = "Newline 0x08"
    conferenceVenue = "Hackerspace.Gent"
    conferenceCity = "Ghent"
    conferenceStart = "2018-04-13"
    conferenceEnd = "2018-04-15"
    conferenceDayChange = "06:00"
    conferenceTimeslotDuration = "00:30"

    startDay = datetime.strptime(conferenceStart, "%Y-%m-%d")
    endDay = datetime.strptime(conferenceEnd, "%Y-%m-%d")
    conferenceDays = int((abs(endDay - startDay)).total_seconds() / (3600 * 24)) + 1

    conf = Conference(
        title=conferenceName,
        venue=conferenceVenue,
        city=conferenceCity,
        start=startDay,
        end=endDay,
        days=conferenceDays,
        day_change=conferenceDayChange,
        timeslot_duration=conferenceTimeslotDuration
        )

    for i in range(0, conferenceDays):
        tempDate = startDay + timedelta(days=i)
        tempDateString = tempDate.strftime("%Y-%m-%d")
        tempDay = Day(tempDate, tempDateString)
        tempDay.add_room(Room(conferenceVenue))
        conf.add_day(tempDay)

    with open(json_input_file) as json_data:
        newline_data = json.load(json_data)

        for event in newline_data:
            tmpEventDate = datetime.fromtimestamp(event['start'])
            tmpEvent = Event(
                title=event['name'],
                description=event['description'],
                type=event['type'],
                duration=time.strftime("%H:%M:%S", time.gmtime(event['duration'])),
                date=tmpEventDate,
                start=tmpEventDate.strftime("%H:%M:%S")
                )

            for day in conf.day_objects:
                if tmpEventDate.strftime("%Y-%m-%d") == day.date.strftime("%Y-%m-%d"):
                    day.room_objects[0].add_event(tmpEvent)

    return conf

def generate_pentabarf_xml(conf_schedule, xml_file):
    """ Generate and write Pentabarf XML file """
    schedule = conf_schedule.generate()

    with open(xml_file, 'w') as xml_export:
        xml_export.write(schedule)

if __name__ == "__main__":
    main()
