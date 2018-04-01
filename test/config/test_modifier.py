#!/usr/bin/python3

import unittest

from devpipeline.config.modifier import modify


class TestConfigModifier(unittest.TestCase):
    def test_simple(self):
        config = {}
        self.assertEqual("foo", modify("foo", config, "name", ""))

    def test_append(self):
        config = {
            "name.append": "bar"
        }
        self.assertEqual("foobar", modify("foo", config, "name", ""))

    def test_prepend(self):
        config = {
            "name.prepend": "bar"
        }
        self.assertEqual("barfoo", modify("foo", config, "name", ""))

    def test_override(self):
        config = {
            "name.override": "bar"
        }
        self.assertEqual("bar", modify("foo", config, "name", ""))

    def test_erase(self):
        config = {
            "name.erase": None
        }
        self.assertEqual(None, modify("foo", config, "name", ""))

    def test_multiple(self):
        config = {
            "name.prepend": "bar",
            "name.append": "baz"
        }
        self.assertEqual("barfoobaz", modify("foo", config, "name", ""))

    def test_finaloverride(self):
        config = {
            "name.preprend": "bar",
            "name.override": "baz"
        }
        self.assertEqual("baz", modify("foo", config, "name", ""))

    def test_finalerase(self):
        config = {
            "name.erase": None,
            "name.override": "baz"
        }
        self.assertEqual(None, modify("foo", config, "name", ""))

    def test_separator(self):
        config = {
            "name.append": "bar"
        }
        self.assertEqual("foo----bar", modify("foo", config, "name", "----"))


if __name__ == "__main__":
    unittest.main()
