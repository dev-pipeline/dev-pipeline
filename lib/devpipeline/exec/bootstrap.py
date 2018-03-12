#!/usr/bin/python3
"""This module does a checkout and build of the packages given in the config file."""
import devpipeline.build.build
import devpipeline.scm.scm
import devpipeline.common


def main(args=None):
    # pylint: disable=bad-continuation,missing-docstring
    builder = devpipeline.common.TargetTool([
        devpipeline.scm.scm.scm_task,
        devpipeline.build.build.build_task
    ],
        prog="dev-pipeline bootstrap",
        description="Checkout and build packages")
    devpipeline.common.execute_tool(builder, args)


if __name__ == '__main__':
    main()
