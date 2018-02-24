#!/usr/bin/python3

import argparse
import errno
import sys

import devpipeline.config
import devpipeline.executor
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


_executor_types = {
    "dry-run": lambda: devpipeline.executor.DryRunExecutor(),
    "quiet": lambda: devpipeline.executor.QuietExecutor(),
    "silent": lambda: devpipeline.executor.SilentExecutor(),
    "verbose": lambda: devpipeline.executor.VerboseExecutor(),
}


class TargetTool(GenericTool):
    def __init__(self, tasks=None, executors=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("targets", nargs="*",
                          help="The targets to operate on")
        self.tasks = tasks
        if executors:
            self.add_argument("--executor",
                              help="The amount of verbosity to use.  Options "
                                   "are \"quiet\" (print no extra "
                                   "information), \"verbose\" (print "
                                   "additional information), \"dry-run\" "
                                   "(print commands to execute, but don't run"
                                   " them), and \"silent\" (print nothing).  "
                                   "Regardless of this option, errors are "
                                   "always printed.",
                              default="quiet")
            self.verbosity = True
        else:
            self.verbosity = False

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)

        self.components = devpipeline.config.rebuild_cache(
            devpipeline.config.find_config())
        if args.targets:
            self.targets = args.targets
        else:
            self.targets = self.components.sections()
        self.setup(args)
        if self.verbosity:
            fn = _executor_types.get(args.executor)
            if not fn:
                raise Exception(
                    "{} isn't a valid executor".format(args.executor))
            else:
                self.executor = fn()
        self.process()

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        self.process_targets(build_order)

    def process_targets(self, build_order):
        for target in build_order:
            self.executor.message("  {}".format(target))
            self.executor.message("-" * (4 + len(target)))
            current = self.components[target]
            for task in self.tasks:
                task(current, target, self.executor)
            self.executor.message("")


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
