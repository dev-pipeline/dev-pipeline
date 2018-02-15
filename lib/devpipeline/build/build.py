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


def build_task(target):
    build_path = target.get("dp.build_dir")
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    builder = make_builder(target)
    builder.configure(target.get("dp.src_dir"), build_path)
    builder.build(build_path)
    if not target.get("no_install"):
        builder.install(build_path, path=target.get("install_path",
                                                    "install"))
