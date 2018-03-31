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
from pytz import timezone
import json
from jsonschema import validate, ValidationError
from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Room import Room
from pentabarf.Event import Event
from pentabarf.Person import Person

def main():
    """ Main function, reads the json file and generates the Pentabarf XML """

    current_year = datetime.now().strftime("%Y")

    json_input_file = '%s/json/data.json' % (current_year)
    json_schema_file = '%s/json/data_schema.json' % (current_year)
    pentabarf_file = '%s/xml/pentabarf.xml' % (current_year)

    try:
        conference = read_json(json_input_file, json_schema_file)
    except IOError as exc:
        print('IOError : %s' % str(exc.message))
        exit()
    except ValueError as exc:
        print('ValueError : %s' % str(exc.message))
        exit()
    except ValidationError as exc:
        print('ValidationError : %s' % str(exc.message))
        exit()

    generate_pentabarf_xml(conference, pentabarf_file)

def read_json(json_input_file, json_schema_file):
    """ Read and parse the conference schedule JSON file """

    # check parameter type
    if not isinstance(json_input_file, str):
        raise TypeError("parameter json_input_file should be a string/path")
    if not isinstance(json_schema_file, str):
        raise TypeError("parameter json_schema_file should be a string/path")

    # check if files exist
    if not isfile(json_input_file):
        raise IOError("Inputfile '%s' does not exist" % json_input_file)
    if not isfile(json_schema_file):
        raise IOError("Schema file '%s' does not exist" % json_schema_file)

    # read event data file
    with open(json_input_file) as json_data:
        try:
            newline_data = json.load(json_data)
        except ValueError:
            raise ValueError(
                "Inputfile '%s' contains invalid JSON" % json_input_file
            )

        # validate conference data json file
        with open(json_schema_file) as json_schema:
            try:
                schema = json.load(json_schema)
            except ValueError:
                raise ValueError(
                    "Schema file '%s' contains invalid JSON" % json_schema_file
                )
            validate(newline_data, schema)

        # read conference data from json file
        timezone_name = newline_data.get('event_timezone') or "Europe/Brussels"
        conf_timezone = timezone(timezone_name)

        start_day = datetime.fromtimestamp(
            float(newline_data.get('event_start')),
            conf_timezone
        )
        end_day = datetime.fromtimestamp(
            float(newline_data.get('event_end')),
            conf_timezone
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

            tmp_event_date = datetime.fromtimestamp(
                float(event.get('start')) - 6*3600, # 6AM day-change
                conf_timezone
            )
            tmp_event_starttime = datetime.fromtimestamp(
                float(event.get('start')),
                conf_timezone
            ).strftime("%H:%M:%S")
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
                start=tmp_event_starttime
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
    if not isinstance(event_rooms, list):
        event_rooms = [event_rooms]

    for event_room in event_rooms:
        # create room if no rooms are defined yet
        day_room_names = [r.name for r in day.room_objects]
        if not event_room in day_room_names:
            day.add_room(Room(event_room))

        for day_room in day.room_objects:
            # add event to room
            if event_room == day_room.name:
                day_room.add_event(event)

def populate_conference_days(conference):
    """ Populate conference with day instances """
    # check parameter type
    if not isinstance(conference, Conference):
        raise TypeError("parameter conference should a Conference instance")

    if not isinstance(conference.days, int):
        raise TypeError("conference.days should be an integer")

    if not isinstance(conference.start, datetime):
        raise TypeError("conference.start should be a datetime instance")

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
