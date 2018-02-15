#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.scm.scm
import devpipeline.common


class Builder(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__([
            devpipeline.scm.scm.scm_task,
            devpipeline.build.build.build_task
        ], description="Checkout and build targets")


builder = Builder()
devpipeline.common.execute_tool(builder)
