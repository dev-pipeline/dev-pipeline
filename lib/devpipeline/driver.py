#!/usr/bin/python3

"""
This module is the driver modules for the execution of various tools.
"""

import argparse

import devpipeline


def _do_list(args):
    del args
    for tool in sorted(devpipeline.TOOLS):
        print("{} - {}".format(tool, devpipeline.TOOLS[tool][1]))


def _main():
    parser = argparse.ArgumentParser(
        "dev-pipeline",
        description="Driver for all dev-pipeline tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title="tool", description="Tool to execute", metavar="<tool>"
    )
    for tool in devpipeline.TOOLS:
        tools_parser = subparsers.add_parser(tool, help=devpipeline.TOOLS[tool][0])
        devpipeline.TOOLS[tool][1](tools_parser)
        tools_parser.set_defaults(func=devpipeline.TOOLS[tool][2])
    # pylint: disable=missing-docstring
    arguments = parser.parse_args()
    if "func" in arguments:
        arguments.func(arguments)
    else:
        parser.parse_args(["--help"])


if __name__ == "__main__":
    _main()
