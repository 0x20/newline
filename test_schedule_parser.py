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

    def test_read_json(self):
        """Test read_json function"""
        # function takes a filename (string) as argument
        self.assertRaises(TypeError, read_json)
        self.assertRaises(TypeError, read_json, 123)
        self.assertRaises(TypeError, read_json, {"test_dict"})
        self.assertRaises(TypeError, read_json, None)

        # function should fail when json file doesn't exist
        self.assertRaises(IOError, read_json, "/path/to/nofile.json")

        # function should fail when file is not valid json
        self.assertRaises(ValueError, read_json, "test/invalid.txt")
        self.assertRaises(ValueError, read_json, "test/invalid.json")

        # function returns a Conference instance if json is valid
        conference = read_json("test/correct_data.json")
        self.assertTrue(isinstance(conference, Conference))

        # conference should have 3 days
        self.assertEqual(3, len(conference.day_objects))


if __name__ == '__main__':
    unittest.main()
