#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.common
import devpipeline.resolve


class Builder(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__([
            devpipeline.build.build.build_task
        ], description="Build targets")


builder = Builder()
devpipeline.common.execute_tool(builder)
