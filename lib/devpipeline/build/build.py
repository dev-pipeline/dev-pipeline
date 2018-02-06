#!/usr/bin/python3

import os
import os.path

import devpipeline.common
import devpipeline.build.cmake
import devpipeline.build.nothing

_builder_lookup = {
    "cmake": devpipeline.build.cmake.make_cmake,
    "nothing": devpipeline.build.nothing.make_nothing
}


def make_builder(component):
    return devpipeline.common.tool_builder(component, "build",
                                           _builder_lookup)


def build_task(target, build_path):
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    builder = make_builder(target)
    builder.configure(target._values["dp_src_dir"], build_path)
    builder.build(build_path)
    if 'no_install' not in target._values:
        builder.install(build_path, path=target._values.get("install_path",
                                                            "install"))


def make_build_task_wrapper(build_dir):
    return lambda t: build_task(t, "{}/{}".format(build_dir, t._name))
