#!/usr/bin/python3

"""
This module is the driver modules for the execution of various tools.
"""

import sys

import devpipeline


def _do_help(args):
    del args
    print("usage: dev-pipeline tool [tool args]")
    print("Arguments:")
    print("\t--help\tDisplay this help")
    print("\t--list\tDisplay available tools")


def _do_list(args):
    del args
    for tool in sorted(devpipeline.TOOLS):
        print("{} - {}".format(tool, devpipeline.TOOLS[tool][1]))


_EX_TOOLS = {"--help": _do_help, "--list": _do_list}


def _find_tool():
    tool = devpipeline.TOOLS.get(sys.argv[1])
    if tool:
        return tool[0]
    return _EX_TOOLS.get(sys.argv[1])


def main():
    # pylint: disable=missing-docstring
    if len(sys.argv) > 1:
        tool = _find_tool()
        if tool:
            tool(sys.argv[2:])
        else:
            print("{} isn't an available tool".format(sys.argv[1]), file=sys.stderr)
            sys.exit(1)
    else:
        _do_help(None)


if __name__ == "__main__":
    main()
