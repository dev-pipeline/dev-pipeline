#!/usr/bin/python3

"""
Tests related to value modification.

These cover the universal modification rules.
"""

import unittest

from devpipeline.config.modifier import modify


class TestConfigModifier(unittest.TestCase):
    """Tests to verify universal modification rules work"""

    def test_simple(self):
        config = {}
        self.assertEqual("foo", modify("foo", config, "name", ""))

    def test_append(self):
        """Verify a single append works"""
        config = {
            "name.append": "bar"
        }
        self.assertEqual("foobar", modify("foo", config, "name", ""))

    def test_prepend(self):
        """Verify a single prepend works"""
        config = {
            "name.prepend": "bar"
        }
        self.assertEqual("barfoo", modify("foo", config, "name", ""))

    def test_override(self):
        """Verify a single override works"""
        config = {
            "name.override": "bar"
        }
        self.assertEqual("bar", modify("foo", config, "name", ""))

    def test_erase(self):
        """Verify a single erase works"""
        config = {
            "name.erase": None
        }
        self.assertEqual(None, modify("foo", config, "name", ""))

    def test_multiple(self):
        """Verify multiple operations work"""
        config = {
            "name.prepend": "bar",
            "name.append": "baz"
        }
        self.assertEqual("barfoobaz", modify("foo", config, "name", ""))

    def test_finaloverride(self):
        """Verify override trumps prepends"""
        config = {
            "name.preprend": "bar",
            "name.override": "baz"
        }
        self.assertEqual("baz", modify("foo", config, "name", ""))

    def test_finalerase(self):
        """Verify override trumps erase"""
        config = {
            "name.erase": None,
            "name.override": "baz"
        }
        self.assertEqual(None, modify("foo", config, "name", ""))

    def test_separator(self):
        """Test a custon separator"""
        config = {
            "name.append": "bar"
        }
        self.assertEqual("foo----bar", modify("foo", config, "name", "----"))


if __name__ == "__main__":
    unittest.main()
