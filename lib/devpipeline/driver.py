#!/usr/bin/python3

"""
This module is the driver modules for the execution of various tools.
"""

import sys

import devpipeline


def _do_help():
    print("usage: dev-pipeline tool [tool args]")
    print("Arguments:")
    print("\t--help\tDisplay this help")
    print("\t--list\tDisplay available tools")


def _do_list():
    for tool in sorted(devpipeline.TOOLS):
        print("{} - {}".format(tool, devpipeline.TOOLS[tool][1]))


_EX_TOOLS = {
    "--help": _do_help,
    "--list": _do_list
}


def main():
    # pylint: disable=missing-docstring
    if len(sys.argv) > 1:
        tool = devpipeline.TOOLS.get(sys.argv[1])
        if tool:
            tool[0](sys.argv[2:])
        else:
            tool = _EX_TOOLS.get(sys.argv[1])
            if tool:
                tool()
            else:
                print("{} isn't an available tool".format(sys.argv[1]))
                sys.exit(1)
    else:
        _do_help()


if __name__ == "__main__":
    main()
