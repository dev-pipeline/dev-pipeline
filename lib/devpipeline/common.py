#!/usr/bin/python3

import argparse
import errno
import sys

import devpipeline.iniloader


class Tool:

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            *args, **kwargs)

        self.add_argument(
            "--config",
            help="Build configuration file",
            default="build.config")
        self.add_argument(
            "--build-dir",
            help="The build folder to use",
            default="build")

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)
        self.components = devpipeline.iniloader.read_config(
            args.config, args.build_dir, "build.config")
        self.build_dir = args.build_dir
        self.setup(args)
        self.process()

    def setup(self, arguments):
        pass

    def process(self):
        pass


def execute_tool(tool):
    try:
        tool.execute()

    except IOError as e:
        if e.errno == errno.EPIPE:
            # This probably means we were piped into something that terminated
            # (e.g., head).  Might be a better way to handle this, but for now
            # silently swallowing the error isn't terrible.
            pass

    except Exception as e:
        print("Error: {}".format(str(e)), file=sys.stderr)
        exit(1)
