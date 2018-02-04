#!/usr/bin/python3

import os
import os.path

import devpipeline.build.cmake
import devpipeline.build.nothing

_builder_lookup = {
    "cmake": devpipeline.build.cmake.make_cmake,
    "nothing": devpipeline.build.nothing.make_nothing
}


def make_builder(component):
    builder = component._values.get("build")
    if builder:
        builder_fn = _builder_lookup.get(builder)
        if builder_fn:
            return builder_fn(component)
        else:
            raise Exception(
                "Unknown builder '{}' for {}".format(builder, component._name))
    else:
        raise Exception("{} does not specify build".format(component._name))


def build_task(target, build_path):
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    builder = make_builder(target)
    builder.configure(target._values["dp_src_dir"], build_path)
    builder.build(build_path)
    if 'no_install' not in target._values:
        builder.install(build_path, path=target._values.get("install_path"))


def make_build_task_wrapper(build_dir):
    return lambda t: build_task(t, "{}/{}".format(build_dir, t._name))
