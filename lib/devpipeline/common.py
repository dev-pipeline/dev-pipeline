#!/usr/bin/python3

import argparse
import errno
import sys

import devpipeline.config
import devpipeline.resolve


class GenericTool:

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            *args, **kwargs)

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)
        self.setup(args)
        self.process()

    def setup(self, arguments):
        pass

    def process(self):
        pass


class TargetTool(GenericTool):
    def __init__(self, tasks=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("targets", nargs="*",
                          help="The targets to operate on")
        self.tasks = tasks

    def execute(self, *args, **kwargs):
        parsed_args = self.parser.parse_args(*args, **kwargs)

        self.components = devpipeline.config.rebuild_cache(
            devpipeline.config.find_config())
        if parsed_args.targets:
            self.targets = parsed_args.targets
        else:
            self.targets = self.components.sections()
        self.setup(parsed_args)
        self.process()

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        self.process_targets(build_order)

    def process_targets(self, build_order):
        for target in build_order:
            current = self.components[target]
            for task in self.tasks:
                task(current)


def execute_tool(tool, args):
    if not args:
        args = sys.argv[1:]
    try:
        tool.execute(args)

    except IOError as e:
        if e.errno == errno.EPIPE:
            # This probably means we were piped into something that terminated
            # (e.g., head).  Might be a better way to handle this, but for now
            # silently swallowing the error isn't terrible.
            pass

    except Exception as e:
        print("Error: {}".format(str(e)), file=sys.stderr)
        exit(1)
