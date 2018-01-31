#!/usr/bin/python3

import devpipeline.common
import devpipeline.resolve


class Builder(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Build a target")
        self.add_argument(
            "targets", nargs="*",
            help="The target to build.")

    def setup(self, arguments):
        self._targets = arguments.targets

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self._targets, self.components)
        print(build_order)


builder = Builder()
devpipeline.common.execute_tool(builder)
