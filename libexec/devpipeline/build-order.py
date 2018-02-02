#!/usr/bin/python3

import devpipeline.common
import devpipeline.resolve


class BuildOrderer(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Determinte all dependencies of a set of"
                                     " targets and the order they should be "
                                     "built in.")
        self.add_argument(
            "targets", nargs="*",
            help="The target to resolve.")

    def setup(self, arguments):
        if not arguments.targets:
            raise Exception("No targets specified")
        else:
            self._targets = arguments.targets

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self._targets, self.components)
        print(build_order)


build_orderer = BuildOrderer()
devpipeline.common.execute_tool(build_orderer)
