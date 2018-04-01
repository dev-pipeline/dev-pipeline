#!/usr/bin/python3

"""The main module for devpipeline"""

import devpipeline.executor

EXECUTOR_TYPES = {
    "dry-run": devpipeline.executor.DryRunExecutor,
    "quiet": devpipeline.executor.QuietExecutor,
    "silent": devpipeline.executor.SilentExecutor,
    "verbose": devpipeline.executor.VerboseExecutor
}
