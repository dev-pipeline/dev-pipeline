#!/usr/bin/python3

import argparse
import errno
import os
import re
import sys

import devpipeline.config.config
import devpipeline.executor
import devpipeline.resolve
import devpipeline.version


class GenericTool:

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            *args, **kwargs)
        self.parser.add_argument("--version", action="version",
                                 version="%(prog)s {}".format(
                                     devpipeline.version.string))

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
    "dry-run": devpipeline.executor.DryRunExecutor,
    "quiet": devpipeline.executor.QuietExecutor,
    "silent": devpipeline.executor.SilentExecutor,
    "verbose": devpipeline.executor.VerboseExecutor
}


def _set_env(env, key, value):
    real_key = key.upper()
    if value:
        env[real_key] = value
    else:
        del env[real_key]


def _append_env(env, key, value):
    real_key = key.upper()
    if real_key in env:
        env[real_key] += "{}{}".format(os.pathsep, value)
    else:
        env[real_key] = value


_env_suffixes = {
    None: _set_env,
    "append": _append_env
}


def _create_target_environment(target):
    ret = os.environ.copy()
    pattern = re.compile(R"^env(?:_(\w+))?\.(\w+)")
    for key, value in target.items():
        m = pattern.match(key)
        if m:
            fn = _env_suffixes.get(m.group(1))
            if fn:
                fn(ret, m.group(2), value)
    return ret


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
        parsed_args = self.parser.parse_args(*args, **kwargs)

        self.components, self.updated = devpipeline.config.config.update_cache()
        if parsed_args.targets:
            self.targets = parsed_args.targets
        else:
            self.targets = self.components.sections()
        self.setup(parsed_args)
        if self.verbosity:
            fn = _executor_types.get(parsed_args.executor)
            if not fn:
                raise Exception(
                    "{} isn't a valid executor".format(parsed_args.executor))
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
            env = _create_target_environment(current)
            for task in self.tasks:
                task(current, self.updated, name=target, env=env, executor=self.executor)
            self.executor.message("")


def execute_tool(tool, args):
    if args is None:
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
