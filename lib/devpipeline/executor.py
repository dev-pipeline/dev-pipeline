#!/usr/bin/python3

import os
import subprocess


class _ExecutorBase:
    # pylint: disable=R0201
    def message(self, msg):
        print(msg)

    # pylint: disable=R0201
    def error(self, msg):
        print("ERROR: {}".format(msg))

    # pylint: disable=R0201
    def warning(self, msg):
        print("WARNING: {}".format(msg))

    def _execute_single(self, environment, **kwargs):
        try:
            subprocess.check_call(env=environment, **kwargs)
        except Exception as e:
            self.error(str(e))

    def execute(self, environment, *args):
        for cmd in args:
            self._execute_single(environment, **cmd)


class QuietExecutor(_ExecutorBase):
    def message(self, msg):
        pass


class SilentExecutor(_ExecutorBase):
    def message(self, msg):
        pass

    def execute(self, environment, *args):
        with open(os.devnull, 'w') as FNULL:
            for cmd in args:
                cmd["stdout"] = FNULL
                self._execute_single(environment, **cmd)


class VerboseExecutor(_ExecutorBase):
    def execute(self, environment, *args):
        for cmd in args:
            cmd_args = cmd.get("args")
            self.message("\tExecuting: {}".format(cmd_args))
            self._execute_single(environment, **cmd)


class DryRunExecutor(_ExecutorBase):
    def execute(self, environment, *args):
        for cmd in args:
            cmd_args = cmd.get("args")
            self.message("\tExecuting: {}".format(cmd_args))
