#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
"""
Unit tests for Schedule parser script

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

import unittest
from schedule_parser import *
from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Room import Room
from pentabarf.Event import Event
from pentabarf.Person import Person

class TestScheduleParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test fixture."""

    def setUp(self):
        """Initialise test environment before each test."""

    def test_read_json_invalid(self):
        """Test read_json function with invalid input """
        # function takes two filenams (string) as argument
        self.assertRaises(TypeError, read_json)
        self.assertRaises(TypeError, read_json, "test")
        self.assertRaises(TypeError, read_json, 123, "test")
        self.assertRaises(TypeError, read_json, {"test_dict"}, "test")
        self.assertRaises(TypeError, read_json, None, "test")
        self.assertRaises(TypeError, read_json, "test", 123)
        self.assertRaises(TypeError, read_json, "test", {"test_dict"})
        self.assertRaises(TypeError, read_json, "test", None)

        # function should fail when json file doesn't exist
        self.assertRaises(
            IOError,
            read_json,
            "/path/to/nofile.json",
            "test/valid_schema.json"
        )
        self.assertRaises(
            IOError,
            read_json,
            "test/valid_data.json",
            "/path/to/nofile.json"
        )

        # function should fail when file is not valid json
        self.assertRaises(
            ValueError,
            read_json,
            "test/invalid.txt",
            "test/valid_schema.json"
        )
        self.assertRaises(
            ValueError,
            read_json,
            "test/invalid.json",
            "test/valid_schema.json"
        )
        self.assertRaises(
            ValueError,
            read_json,
            "test/valid_data.json",
            "test/invalid.txt"
        )
        self.assertRaises(
            ValueError,
            read_json,
            "test/valid_data.json",
            "test/invalid.json"
        )

    def test_read_json_missing_parameters(self):
        """Test read_json function with missing parameters in json file  """
        self.assertRaises(
            ValidationError,
            read_json,
            "test/invalid_data_missing_parameters.json",
            "test/valid_schema.json"
        )

    def test_read_json_invalid_parameters(self):
        """Test read_json function with invalid parameter values in json file  """
        self.assertRaises(
            ValidationError,
            read_json,
            "test/invalid_data_invalid_parameters.json",
            "test/valid_schema.json"
        )

    def test_read_json_valid(self):
        """Test read_json function with valid input """
        # function returns a Conference instance if json is valid
        conference = read_json("test/valid_data.json", "test/valid_schema.json")
        self.assertTrue(isinstance(conference, Conference))

        # checks conference parameters
        self.assertEqual("Newline 0x08", conference.title)
        self.assertEqual("hackerspace.gent", conference.venue)
        self.assertEqual("Ghent", conference.city)
        self.assertEqual(3, conference.days)
        self.assertEqual("06:00", conference.day_change)
        self.assertEqual("00:30", conference.timeslot_duration)
        self.assertTrue(isinstance(conference.start, datetime))
        self.assertEqual("2018-04-13", conference.start.strftime("%Y-%m-%d"))
        self.assertTrue(isinstance(conference.end, datetime))
        self.assertEqual("2018-04-15", conference.end.strftime("%Y-%m-%d"))

        # conference should have 3 days
        self.assertEqual(3, len(conference.day_objects))

        # check first day
        firstday = conference.day_objects[0]
        self.assertTrue(isinstance(firstday.date, datetime))
        self.assertEqual("2018-04-13", firstday.date.strftime("%Y-%m-%d"))
        self.assertEqual(1, len(firstday.room_objects))

        # check room 1 on first day
        test_room = firstday.room_objects[0]
        self.assertTrue(isinstance(test_room, Room))
        self.assertEqual("1.21", test_room.name)
        self.assertEqual(1, len(test_room.event_objects))

        # check event 1
        test_event = test_room.event_objects[0]
        self.assertTrue(isinstance(test_event, Event))
        self.assertEqual(1, test_event.id)
        self.assertEqual("Retro games, arcade and music night", test_event.title)
        self.assertEqual("general", test_event.type)
        self.assertEqual(
            "We'll set up some old consoles, arcades and have fun!",
            test_event.description
        )
        self.assertEqual("09:00:00", test_event.duration)
        self.assertTrue(isinstance(test_event.date, datetime))
        self.assertEqual("2018-04-13", test_event.date.strftime("%Y-%m-%d"))
        self.assertEqual("18:00:00", test_event.start)
        self.assertEqual(2, len(test_event.person_objects))

        # check first speaker
        test_speaker = test_event.person_objects[0]
        self.assertTrue(isinstance(test_speaker, Person))
        self.assertEqual("speaker 1", test_speaker.name)

        # check second speaker
        test_speaker = test_event.person_objects[1]
        self.assertTrue(isinstance(test_speaker, Person))
        self.assertEqual("speaker 2", test_speaker.name)

        # check second day
        secondday = conference.day_objects[1]
        self.assertTrue(isinstance(secondday.date, datetime))
        self.assertEqual("2018-04-14", secondday.date.strftime("%Y-%m-%d"))
        self.assertEqual(3, len(secondday.room_objects))

        # check room 1 on second day
        test_room = secondday.room_objects[0]
        self.assertTrue(isinstance(test_room, Room))
        self.assertEqual("hackerspace.gent", test_room.name)
        self.assertEqual(1, len(test_room.event_objects))

        # check event 2
        test_event = test_room.event_objects[0]
        self.assertTrue(isinstance(test_event, Event))
        self.assertEqual(2, test_event.id)
        self.assertEqual("Welcome!", test_event.title)
        self.assertEqual("talk", test_event.type)
        self.assertEqual(
            "An introduction to the Hackerspace and Newline!",
            test_event.description
        )
        self.assertEqual("01:00:00", test_event.duration)
        self.assertTrue(isinstance(test_event.date, datetime))
        self.assertEqual("2018-04-14", test_event.date.strftime("%Y-%m-%d"))
        self.assertEqual("13:00:00", test_event.start)
        self.assertEqual(1, len(test_event.person_objects))

        # check first speaker
        test_speaker = test_event.person_objects[0]
        self.assertTrue(isinstance(test_speaker, Person))
        self.assertEqual("speaker 3", test_speaker.name)

        # check room 2 on second day
        test_room = secondday.room_objects[1]
        self.assertTrue(isinstance(test_room, Room))
        self.assertEqual("1.21", test_room.name)
        self.assertEqual(1, len(test_room.event_objects))

        # check event 3
        test_event = test_room.event_objects[0]
        self.assertTrue(isinstance(test_event, Event))
        self.assertEqual(3, test_event.id)
        self.assertEqual("Welcome 2 workshops!", test_event.title)
        self.assertEqual("workshop", test_event.type)
        self.assertEqual(
            "Workshops in 2 other rooms",
            test_event.description
        )
        self.assertEqual("01:00:00", test_event.duration)
        self.assertTrue(isinstance(test_event.date, datetime))
        self.assertEqual("2018-04-14", test_event.date.strftime("%Y-%m-%d"))
        self.assertEqual("13:00:00", test_event.start)
        self.assertEqual(0, len(test_event.person_objects))

        # check room 3 on second day
        test_room = secondday.room_objects[2]
        self.assertTrue(isinstance(test_room, Room))
        self.assertEqual("1.22", test_room.name)
        self.assertEqual(1, len(test_room.event_objects))

        # check event 3
        test_event = test_room.event_objects[0]
        self.assertTrue(isinstance(test_event, Event))
        self.assertEqual(3, test_event.id)
        self.assertEqual("Welcome 2 workshops!", test_event.title)
        self.assertEqual("workshop", test_event.type)
        self.assertEqual(
            "Workshops in 2 other rooms",
            test_event.description
        )
        self.assertEqual("01:00:00", test_event.duration)
        self.assertTrue(isinstance(test_event.date, datetime))
        self.assertEqual("2018-04-14", test_event.date.strftime("%Y-%m-%d"))
        self.assertEqual("13:00:00", test_event.start)
        self.assertEqual(0, len(test_event.person_objects))

        # check third day
        thirdday = conference.day_objects[2]
        self.assertTrue(isinstance(thirdday.date, datetime))
        self.assertEqual("2018-04-15", thirdday.date.strftime("%Y-%m-%d"))
        self.assertEqual(0, len(thirdday.room_objects))

    def test_populate_conference_days_invalid_parameters(self):
        """ Test populate_conference_days """
        self.assertRaises(TypeError, populate_conference_days)
        self.assertRaises(TypeError, populate_conference_days, "string")
        self.assertRaises(TypeError, populate_conference_days, 123)
        self.assertRaises(TypeError, populate_conference_days, {})

        conference = Conference()
        self.assertRaises(TypeError, populate_conference_days, conference)

        conference = Conference(
            start=datetime(2018, 3, 4)
        )
        self.assertRaises(TypeError, populate_conference_days, conference)

    def test_populate_conference_days_0day(self):
        """ Test populate_conference_days """
        conference = Conference(
            start=datetime(2018, 3, 4),
            end=datetime(2018, 3, 4),
            days=0
        )

        self.assertEqual(0, len(conference.day_objects))
        populate_conference_days(conference)
        self.assertEqual(0, len(conference.day_objects))

    def test_populate_conference_days_1day(self):
        """ Test populate_conference_days """
        conference = Conference(
            start=datetime(2018, 3, 4),
            end=datetime(2018, 3, 4),
            days=1
        )

        self.assertEqual(0, len(conference.day_objects))
        populate_conference_days(conference)
        self.assertEqual(1, len(conference.day_objects))

        # check first day
        test_day = conference.day_objects[0]
        self.assertTrue(isinstance(test_day.date, datetime))
        self.assertEqual("2018-03-04", test_day.date.strftime("%Y-%m-%d"))


    def test_populate_conference_days_4days(self):
        """ Test populate_conference_days """
        conference = Conference(
            start=datetime(2018, 3, 4),
            end=datetime(2018, 3, 7),
            days=4
        )

        self.assertEqual(0, len(conference.day_objects))
        populate_conference_days(conference)
        self.assertEqual(4, len(conference.day_objects))

        # check first day
        test_day = conference.day_objects[0]
        self.assertTrue(isinstance(test_day.date, datetime))
        self.assertEqual("2018-03-04", test_day.date.strftime("%Y-%m-%d"))

        # check second day
        test_day = conference.day_objects[1]
        self.assertTrue(isinstance(test_day.date, datetime))
        self.assertEqual("2018-03-05", test_day.date.strftime("%Y-%m-%d"))

        # check third day
        test_day = conference.day_objects[2]
        self.assertTrue(isinstance(test_day.date, datetime))
        self.assertEqual("2018-03-06", test_day.date.strftime("%Y-%m-%d"))

        # check fourth day
        test_day = conference.day_objects[3]
        self.assertTrue(isinstance(test_day.date, datetime))
        self.assertEqual("2018-03-07", test_day.date.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    unittest.main()
