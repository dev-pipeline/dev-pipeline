#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.scm.scm
import devpipeline.common
import devpipeline.resolve


class Builder(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__(description="Checkout and build targets")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        self.process_targets(build_order, [
            devpipeline.scm.scm.scm_task,
            devpipeline.build.build.build_task
        ])


builder = Builder()
devpipeline.common.execute_tool(builder)
