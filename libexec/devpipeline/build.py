#!/usr/bin/python3

import operator

import devpipeline.common
import devpipeline.iniloader


class Builder(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Build a target")
        self.add_argument(
            "--target",
            help="The target to build.")

    def setup(self, arguments):
        self._components = devpipeline.iniloader.read_config(arguments.config)

    def process(self):
        for name, component in self._components._components.items():
            print("{} : {}".format(name, component._values["depends"]))


builder = Builder()
devpipeline.common.execute_tool(builder)
