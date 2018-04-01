#!/usr/bin/python3

import unittest

import devpipeline.toolsupport


class TestFlexArgs(unittest.TestCase):
    def validate(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for index, value in enumerate(expected):
            self.assertEqual(value, actual[index])

    def test_simple(self):
        expected = [
            "foo.bar",
            "foo.baz"
        ]
        expanded = devpipeline.toolsupport.build_flex_args_keys([
            ["foo"],
            ["bar", "baz"]
        ])
        self.validate(expected, expanded)

    def test_complex(self):
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
        self.validate(expected, expanded)


if __name__ == "__main__":
    unittest.main()
