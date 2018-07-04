#!/usr/bin/python3
"""This module is the driver modules for the execution of various tools."""

import sys

import devpipeline.plugin


def _do_help():
    print("usage: dev-pipeline tool [tool args]")
    print("Arguments:")
    print("\t--help\tDisplay this help")
    print("\t--list\tDisplay available tools")


_TOOLS = None


def _initialize_tools():
    global _TOOLS

    if not _TOOLS:
        _TOOLS = devpipeline.plugin.query_plugins('devpipeline.drivers')


def _do_list():
    _initialize_tools()
    for tool in _TOOLS:
        print(tool)


_EX_TOOLS = {
    "--help": _do_help,
    "--list": _do_list
}


def main():
    # pylint: disable=missing-docstring
    _initialize_tools()
    if len(sys.argv) > 1:
        tool = _TOOLS.get(sys.argv[1])
        if tool:
            tool(sys.argv[2:])
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
