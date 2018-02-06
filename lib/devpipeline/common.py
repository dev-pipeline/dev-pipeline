#!/usr/bin/python3

import os.path
import argparse
import errno
import re
import sys

import devpipeline.iniloader


def _get_context(args):
    if args.context:
        config = devpipeline.iniloader.read_config(
            "{}/{}".format(os.path.expanduser("~"), ".dev-pipeline"))
        context = config._components.get(args.context)
        if not context:
            raise Exception("Unable to load context {}".format(args.context))
        return context
    return None


class Tool:

    def __init__(self, targets=True, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            *args, **kwargs)

        self.add_argument(
            "--config",
            help="Build configuration file",
            default="build.config")
        self.add_argument(
            "--context",
            help="Build-specific context to use")
        self.add_argument(
            "--build-dir",
            help="The build folder to use",
            default="build")
        if targets:
            self.add_argument(
                "targets", nargs="*",
                help="The targets to operate on")

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)
        context_config = _get_context(args)
        if context_config:
            self.build_dir = "{}-{}".format(args.build_dir, args.context)
        else:
            self.build_dir = args.build_dir
        if "targets" in args:
            if not args.targets:
                raise Exception("No targets specified")
            else:
                self.targets = args.targets
        self.components = devpipeline.iniloader.read_config(
            args.config,
            cache_path="{}/{}".format(self.build_dir, "config.cache"),
            context=context_config)
        self.setup(args)
        self.process()

    def setup(self, arguments):
        pass

    def process(self):
        pass

    def process_targets(self, targets, tasks):
        for target in targets:
            current = self.components._components[target]
            for task in tasks:
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
    tool_name = component._values.get(key)
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
    for key, value in component._values.items():
        m = pattern.match(key)
        if m:
            real_key = key[m.end():]
            hit = args_dict.get(real_key)
            if hit:
                val_found_fn(value, hit)
