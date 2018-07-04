#!/usr/bin/python3
"""This module initiates the build."""

import devpipeline_core.command

import devpipeline.build


def main(args=None):
    # pylint: disable=missing-docstring
    builder = devpipeline_core.command.TargetTool([
        devpipeline.build.build_task
    ], prog="dev-pipeline build", description="Build targets")
    devpipeline_core.command.execute_tool(builder, args)


if __name__ == '__main__':
    main()
