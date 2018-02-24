#!/usr/bin/python3

import sys

import devpipeline.exec.bootstrap
import devpipeline.exec.build
import devpipeline.exec.build_order
import devpipeline.exec.checkout
import devpipeline.exec.configure


def _do_help():
    print("usage: dev-pipeline tool [tool args]")
    print("Arguments:")
    print("\t--help\tDisplay this help")
    print("\t--list\tDisplay available tools")


_tools = {
    "bootstrap": devpipeline.exec.bootstrap.main,
    "build-order": devpipeline.exec.build_order.main,
    "build": devpipeline.exec.build.main,
    "checkout": devpipeline.exec.checkout.main,
    "configure": devpipeline.exec.configure.main
}


def _do_list():
    for tool in _tools:
        print(tool)


_ex_tools = {
    "--help": _do_help,
    "--list": _do_list
}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tool = _tools.get(sys.argv[1])
        if tool:
            tool(sys.argv[2:])
        else:
            tool = _ex_tools.get(sys.argv[1])
            if tool:
                tool()
            else:
                print("{} isn't an available tool")
                sys.exit(1)
    else:
        _do_help()
