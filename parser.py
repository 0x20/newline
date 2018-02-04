#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:

from os.path import isfile
from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Room import Room
from pentabarf.Event import Event
from datetime import date, datetime, timedelta
import time
import json

jsonInputFile = '2018/json/data.json'
pentabarfFile = '2018/xml/pentabarf.xml'

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
        tmpEventDate=datetime.fromtimestamp(event['start'])
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
