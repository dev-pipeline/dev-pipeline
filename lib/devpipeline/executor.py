#!/usr/bin/python3

import os
import subprocess


class _ExecutorBase:
    def message(self, msg):
        print(msg)

    def error(self, msg):
        print("ERROR: {}".format(msg))

    def warning(self, msg):
        print("WARNING: {}".format(msg))


class QuietExecutor(_ExecutorBase):
    def message(self, msg):
        pass

    def execute(self, **kwargs):
        subprocess.check_call(**kwargs)


class SilentExecutor(_ExecutorBase):
    def message(self, msg):
        pass

    def execute(self, **kwargs):
        with open(os.devnull, 'w') as FNULL:
            kwargs["stdout"] = FNULL
            subprocess.check_call(**kwargs)


class VerboseExecutor(_ExecutorBase):
    def execute(self, **kwargs):
        args = kwargs.get("args")
        self.message("\tExecuting: {}".format(args))
        subprocess.check_call(**kwargs)


class DryRunExecutor(_ExecutorBase):
    def execute(self, **kwargs):
        args = kwargs.get("args")
        self.message("\tExecuting: {}".format(args))
