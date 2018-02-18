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
from datetime import datetime, timedelta
import time
import json
from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Room import Room
from pentabarf.Event import Event
from pentabarf.Person import Person

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
            venue=newline_data.get('event_venue') or "Venue",
            city=newline_data.get('event_city') or "City",
            start=start_day,
            end=end_day,
            days=conference_days,
            day_change='06:00',
            timeslot_duration='00:30'
        )

        populate_conference_days(conf)

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

            # create event
            tmp_event = Event(
                id=event.get('id'),
                title=event.get('name'),
                description=event.get('description'),
                type=event.get('type'),
                duration=tmp_duration,
                date=tmp_event_date,
                start=tmp_event_date.strftime("%H:%M:%S")
            )

            # add speakers to event
            for speaker in event.get('speakers'):
                tmp_event.add_person(Person(name=speaker))

            add_event2conference(
                conf,
                tmp_event,
                event.get('rooms')
            )

    return conf

def add_event2conference(conference, event, event_rooms):
    """ Add event to a conference """
    # look for to the correct conference day
    for conf_day in conference.day_objects:
        if event.date.strftime("%Y-%m-%d") \
            == conf_day.date.strftime("%Y-%m-%d"):

            add_event2day(conference, conf_day, event, event_rooms)

def add_event2day(conference, day, event, event_rooms):
    """ Add event to a conference day """
    # use conference venue as default room
    if not event_rooms:
        event_rooms = [conference.venue]

    # event_rooms should be a list
    if type(event_rooms) is not list:
        event_rooms = [event_rooms]

    for event_room in event_rooms:
        # create room if no rooms are defined yet
        if not day.room_objects:
            day.add_room(Room(event_room))

        for day_room in day.room_objects:
            # add event room if it doesn't exist for the conference day
            if not day_room.name in event_rooms:
                day.add_room(Room(event_room))

            # add event to room
            if event_room == day_room.name:
                day_room.add_event(event)

def populate_conference_days(conference):
    """ Populate conference with day instances """
    for i in range(0, conference.days):
        tmp_date = conference.start + timedelta(days=i)
        tmp_date_string = tmp_date.strftime("%Y-%m-%d")
        tmp_day = Day(tmp_date, tmp_date_string)
        conference.add_day(tmp_day)

def generate_pentabarf_xml(conf_schedule, xml_file):
    """ Generate and write Pentabarf XML file """
    schedule = conf_schedule.generate()

    with open(xml_file, 'w') as xml_export:
        xml_export.write(schedule)

if __name__ == "__main__":
    main()
