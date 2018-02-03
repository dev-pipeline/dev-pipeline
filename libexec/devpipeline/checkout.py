#!/usr/bin/python3

import devpipeline.scm.scm
import devpipeline.common
import devpipeline.resolve


class Checkout(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Checkout repositories")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        for target in build_order:
            scm = devpipeline.scm.scm.make_scm(
                self.components._components[target])
            scm.checkout(target)
            scm.update(target)


checkout = Checkout()
devpipeline.common.execute_tool(checkout)
