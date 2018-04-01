#!/usr/bin/python3

"""Verify override configurations can modify a project"""

import os.path
import unittest

import devpipeline.config.override
import devpipeline.config.paths

_CONFIG_DIR = "{}/../files".format(os.path.dirname(os.path.abspath(__file__)))


def _load_overrides(target, override_list, found_fn):
    overrides = devpipeline.config.override.read_overrides(
        devpipeline.config.paths.get_overrides_root(_CONFIG_DIR),
        target, override_list)
    return devpipeline.config.override.apply_all_overrides(
        overrides, found_fn)


class TestConfigOverride(unittest.TestCase):
    """Tests to validate overrie configurations modify a project correctly"""

    def _validate(self, expected, override, actual):
        self.assertTrue(override in expected)
        expected_overrides = expected[override]
        self.assertEqual(len(expected_overrides), len(actual))
        for key, value in expected_overrides.items():
            self.assertTrue(key in actual)
            self.assertEqual(value, actual[key])

    def test_empty(self):
        """Verify an empty override configuraiton has no impact"""
        def _dont_call(override, values):
            # pylint: disable=unused-argument
            raise Exception("Shouldn't have been called")

        count = _load_overrides("foo", ["empty"], _dont_call)
        self.assertEqual(0, count)

    def test_append(self):
        """Verify a single "append" section works correctly"""
        expected = {
            "simple": {
                "val.append": "abc",
                "lav.append": "xyz"
            }
        }

        count = _load_overrides(
            "foo", ["simple"],
            lambda override, vals: self._validate(
                expected, override, vals))
        self.assertEqual(1, count)

    def test_multiappend(self):
        """Verify multiple "append" sections works correctly"""
        expected = {
            "simple": {
                "val.append": "abc",
                "lav.append": "xyz"
            },
            "trivial": {
                "val.append": "ijk"
            }
        }

        count = _load_overrides(
            "foo", ["simple", "trivial"],
            lambda override, vals: self._validate(
                expected, override, vals))
        self.assertEqual(2, count)


if __name__ == "__main__":
    unittest.main()
