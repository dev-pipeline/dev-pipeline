#!/usr/bin/python3

import os
import os.path

import devpipeline.build.cmake
import devpipeline.common


# Every builder supported should have an entry in this dictionary.  The key
# needs to match whatever value the "build" key is set to in build.conf, and
# the value should be a function that takes a component and returns a Builder.
_builder_lookup = {
    "cmake": devpipeline.build.cmake.make_cmake,
    "nothing": lambda c: devpipeline.build.Builder()
}


def _make_builder(component):
    """
    Create and return a Builder for a component.

    Arguments
    component - The component the builder should be created for.
    """
    return devpipeline.common.tool_builder(component, "build",
                                           _builder_lookup)


def build_task(target):
    """
    Build a target.

    Arguments
    target - The target to build.
    """

    build_path = target.get("dp.build_dir")
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    builder = _make_builder(target)
    builder.configure(target.get("dp.src_dir"), build_path)
    builder.build(build_path)
    if not target.get("no_install"):
        builder.install(build_path, path=target.get("install_path",
                                                    "install"))
