#!/usr/bin/python3

"""Test flexible argument building"""

import unittest

import devpipeline.toolsupport


class TestFlexArgs(unittest.TestCase):
    """Tests related to flex arguments"""

    def _validate(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for index, value in enumerate(expected):
            self.assertEqual(value, actual[index])

    def test_simple(self):
        """Verify one level of expansion works"""
        expected = [
            "foo.bar",
            "foo.baz"
        ]
        expanded = devpipeline.toolsupport.build_flex_args_keys([
            ["foo"],
            ["bar", "baz"]
        ])
        self._validate(expected, expanded)

    def test_complex(self):
        """Verify multiple levels of expansion work"""
        expected = [
            "foo.bar.baz",
            "foo.bar.bing",
            "foo.oof.baz",
            "foo.oof.bing"
        ]
        expanded = devpipeline.toolsupport.build_flex_args_keys([
            ["foo"],
            ["bar", "oof"],
            ["baz", "bing"]
        ])
        self._validate(expected, expanded)


if __name__ == "__main__":
    unittest.main()
