import devpipeline.executor

EXECUTOR_TYPES = {
    "dry-run": executor.DryRunExecutor,
    "quiet": executor.QuietExecutor,
    "silent": executor.SilentExecutor,
    "verbose": executor.VerboseExecutor
}
