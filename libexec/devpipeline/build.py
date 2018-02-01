#!/usr/bin/python3

import os
import os.path

import devpipeline.common
import devpipeline.cmake
import devpipeline.resolve

_builder_lookup = {
    "cmake": devpipeline.cmake.make_cmake
}


def make_builder(target, components, build_dir):
    component = components._components[target]
    if "build" in component._values:
        builder = component._values["build"]
        if builder in _builder_lookup:
            return _builder_lookup[builder](component, build_dir)
        else:
            raise Exception(
                "Unknown builder '{}' for {}".format(builder, target))
    else:
        raise Exception("{} does not specify build".format(target))


class Builder(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Build a target")
        self.add_argument(
            "targets", nargs="*",
            help="The target to build.")
        self.add_argument(
            "--build-dir",
            help="The build folder to use",
            default="build")

    def setup(self, arguments):
        self._targets = arguments.targets
        self._build_dir = arguments.build_dir

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self._targets, self.components)
        pwd = os.getcwd()
        for target in build_order:
            build_path = "{}/{}".format(self._build_dir, target)
            if not os.path.exists(build_path):
                os.makedirs(build_path)
            builder = make_builder(target, self.components, build_path)
            builder.configure("{}/{}".format(pwd, target))
            builder.build()
            builder.install()


builder = Builder()
devpipeline.common.execute_tool(builder)
