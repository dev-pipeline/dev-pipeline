#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.common


builder = devpipeline.common.TargetTool([
    devpipeline.build.build.build_task
], description="Build targets")
devpipeline.common.execute_tool(builder)
