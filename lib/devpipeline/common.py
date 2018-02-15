#!/usr/bin/python3

import argparse
import errno
import re
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
    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("targets", nargs="*",
                          help="The targets to operate on")
        self.tasks = tasks

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)

        config = devpipeline.config.find_config()
        self.components = config.read_config()
        if args.targets:
            self.targets = args.targets
        else:
            self.targets = self.components.sections()
        self.setup(args)
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


def tool_builder(component, key, tool_map):
    tool_name = component.get(key)
    if tool_name:
        tool_fn = tool_map.get(tool_name)
        if tool_fn:
            return tool_fn(component)
        else:
            raise Exception(
                "Unknown {} '{}' for {}".format(key, tool_name, component._name))
    else:
        raise Exception("{} does not specify {}".format(component._name, key))


def args_builder(prefix, component, args_dict, val_found_fn):
    pattern = re.compile(R"^{}\.".format(prefix))
    for key, value in component.items():
        m = pattern.match(key)
        if m:
            real_key = key[m.end():]
            hit = args_dict.get(real_key)
            if hit:
                val_found_fn(value, hit)
