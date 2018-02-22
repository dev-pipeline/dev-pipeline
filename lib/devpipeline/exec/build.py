#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.common


if __name__ == '__main__':
    builder = devpipeline.common.TargetTool([
        devpipeline.build.build.build_task
    ], description="Build targets")
    devpipeline.common.execute_tool(builder)
