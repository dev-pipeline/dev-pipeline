#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.scm.scm
import devpipeline.common
import devpipeline.resolve


class Builder(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(targets=False,
                         description="Checkout and build targets")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.components._components.keys(), self.components)
        self.process_targets(build_order, [
            devpipeline.scm.scm.scm_task,
            devpipeline.build.build.make_build_task_wrapper(self.build_dir)
        ])


builder = Builder()
devpipeline.common.execute_tool(builder)
