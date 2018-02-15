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

    with open(json_input_file) as json_data:
        newline_data = json.load(json_data)

        # read conference data from json file
        conference_venue = newline_data.get('event_venue') or "Venue"
        start_day = datetime.fromtimestamp(
            float(newline_data.get('event_start'))
        )
        end_day = datetime.fromtimestamp(
            float(newline_data.get('event_end'))
        )
        conference_days = 1 + int(
            (abs(end_day - start_day)).total_seconds() / (3600 * 24)
        )

        # create conference instance
        conf = Conference(
            title=newline_data.get('event_name') or "Event Name",
            venue=conference_venue,
            city=newline_data.get('event_city') or "City",
            start=start_day,
            end=end_day,
            days=conference_days,
            day_change='06:00',
            timeslot_duration='00:30'
        )

        # create day instances
        for i in range(0, conference_days):
            tmp_date = start_day + timedelta(days=i)
            tmp_date_string = tmp_date.strftime("%Y-%m-%d")
            tmp_day = Day(tmp_date, tmp_date_string)
            tmp_day.add_room(Room(conference_venue))
            conf.add_day(tmp_day)

        # loop over events in json data file to create schedule instances
        for event in newline_data.get('event_schedule'):
            # only add event if the scheduled status is final
            # else jump to the next event
            if not event.get('scheduled') == 'final':
                continue

            tmp_event_date = datetime.fromtimestamp(float(event.get('start')))
            tmp_duration = time.strftime(
                "%H:%M:%S",
                time.gmtime(event.get('duration'))
            )

            tmp_event = Event(
                id=event.get('id'),
                title=event.get('name'),
                description=event.get('description'),
                type=event.get('type'),
                duration=tmp_duration,
                date=tmp_event_date,
                start=tmp_event_date.strftime("%H:%M:%S")
                )

            # add event to correct day
            for day in conf.day_objects:
                if tmp_event_date.strftime("%Y-%m-%d") == day.date.strftime("%Y-%m-%d"):
                    day.room_objects[0].add_event(tmp_event)

    return conf

def generate_pentabarf_xml(conf_schedule, xml_file):
    """ Generate and write Pentabarf XML file """
    schedule = conf_schedule.generate()

    with open(xml_file, 'w') as xml_export:
        xml_export.write(schedule)

if __name__ == "__main__":
    main()
