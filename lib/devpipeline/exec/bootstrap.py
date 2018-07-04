#!/usr/bin/python3
"""This module does a checkout and build of the packages given in the config file."""
import devpipeline_core.command

import devpipeline.build
import devpipeline.scm


def main(args=None):
    # pylint: disable=bad-continuation,missing-docstring
    builder = devpipeline_core.command.TargetTool([
        devpipeline.scm.scm_task,
        devpipeline.build.build_task
    ],
        prog="dev-pipeline bootstrap",
        description="Checkout and build packages")
    devpipeline_core.command.execute_tool(builder, args)


if __name__ == '__main__':
    main()
