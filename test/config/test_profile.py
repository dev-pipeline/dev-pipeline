#!/usr/bin/python3

import os.path
import unittest

import loader

import devpipeline.config.paths
import devpipeline.config.profile

_config_dir = "{}/../files".format(os.path.dirname(os.path.abspath(__file__)))


class TestConfigProfile(unittest.TestCase):
    def _validate(self, expected, override, actual):
        self.assertTrue(override in expected)
        expected_overrides = expected[override]
        self.assertEqual(len(expected_overrides), len(actual))
        for key, value in expected_overrides.items():
            self.assertTrue(key in actual)
            self.assertEqual(value, actual[key])

    def test_none(self):
        def _dont_call(profile, values):
            raise Exception("Shouldn't have been called")

        count = devpipeline.config.profile.read_all_profiles(
            devpipeline.config.paths.get_profile_path(_config_dir), [], _dont_call)
        self.assertEqual(0, count)

    def test_single(self):
        expected = {
            "debug": {
                "build_type": "Debug"
            }
        }

        count = devpipeline.config.profile.read_all_profiles(
            devpipeline.config.paths.get_profile_path(_config_dir), ["debug"],
            lambda p, v: self._validate(expected, p, v))
        self.assertEqual(1, count)

    def test_multiple(self):
        expected = {
            "debug": {
                "build_type": "Debug"
            },
            "clang": {
                "cc": "clang",
                "cxx": "clang++"
            }
        }

        count = devpipeline.config.profile.read_all_profiles(
            devpipeline.config.paths.get_profile_path(_config_dir), [
                "debug", "clang"],
            lambda p, v: self._validate(expected, p, v))
        self.assertEqual(2, count)


if __name__ == "__main__":
    unittest.main()
