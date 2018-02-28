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

    def execute(self, environment, **kwargs):
        try:
            subprocess.check_call(env=environment, **kwargs)
        except Exception as e:
            self.error(str(e))


class QuietExecutor(_ExecutorBase):
    def message(self, msg):
        pass


class SilentExecutor(_ExecutorBase):
    def message(self, msg):
        pass

    def execute(self, environment, **kwargs):
        with open(os.devnull, 'w') as FNULL:
            kwargs["stdout"] = FNULL
            super(SilentExecutor, self).execute(environment, **kwargs)


class VerboseExecutor(_ExecutorBase):
    def execute(self, environment, **kwargs):
        args = kwargs.get("args")
        self.message("\tExecuting: {}".format(args))
        super(VerboseExecutor, self).execute(environment, **kwargs)


class DryRunExecutor(_ExecutorBase):
    def execute(self, environment, **kwargs):
        args = kwargs.get("args")
        super(DryRunExecutor, self).message("\tExecuting: {}".format(args))
