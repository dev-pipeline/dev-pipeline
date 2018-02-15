#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.common
import devpipeline.resolve


class Builder(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__(description="Build targets")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        self.process_targets(build_order, [
            devpipeline.build.build.build_task
        ])


builder = Builder()
devpipeline.common.execute_tool(builder)
