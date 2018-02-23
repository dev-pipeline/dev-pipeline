#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.common


def main(args=None):
    builder = devpipeline.common.TargetTool([
        devpipeline.build.build.build_task
    ], description="Build targets")
    devpipeline.common.execute_tool(builder, args)


if __name__ == '__main__':
    main()
