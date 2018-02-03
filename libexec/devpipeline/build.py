#!/usr/bin/python3

import os
import os.path

import devpipeline.common
import devpipeline.build.build
import devpipeline.resolve


class Builder(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Build a target")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        pwd = os.getcwd()
        for target in build_order:
            component = self.components._components[target]
            build_path = "{}/{}".format(self.build_dir, target)
            if not os.path.exists(build_path):
                os.makedirs(build_path)
            builder = devpipeline.build.build.make_builder(
                component, build_path)
            builder.configure("{}/{}".format(pwd, target))
            builder.build()
            if 'no_install' not in component._values:
                builder.install(path=component._values.get("install_path"))


builder = Builder()
devpipeline.common.execute_tool(builder)
