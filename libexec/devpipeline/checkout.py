#!/usr/bin/python3

import devpipeline.scm.scm
import devpipeline.common
import devpipeline.resolve


class Checkout(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__(description="Checkout repositories")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        self.process_targets(build_order, [
            devpipeline.scm.scm.scm_task
        ])


checkout = Checkout()
devpipeline.common.execute_tool(checkout)
