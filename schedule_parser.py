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

CURRENT_YEAR = datetime.now().strftime("%Y")

jsonInputFile = '%s/json/data.json' % (CURRENT_YEAR)
pentabarfFile = '%s/xml/pentabarf.xml' % (CURRENT_YEAR)

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

if not isfile(jsonInputFile):
    print "Inputfile '%s' does not exist" % jsonInputFile
    exit()

with open(jsonInputFile) as json_data:
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

    schedule = conf.generate()

    with open(pentabarfFile, 'w') as xml_export:
        xml_export.write(schedule)
