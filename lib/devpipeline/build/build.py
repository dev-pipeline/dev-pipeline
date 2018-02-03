#!/usr/bin/python3

import devpipeline.build.cmake

_builder_lookup = {
    "cmake": devpipeline.build.cmake.make_cmake
}


def make_builder(component, build_dir):
    builder = component._values.get("build")
    if builder:
        builder_fn = _builder_lookup.get(builder)
        if builder_fn:
            return builder_fn(component, build_dir)
        else:
            raise Exception(
                "Unknown builder '{}' for {}".format(builder, component._name))
    else:
        raise Exception("{} does not specify build".format(component._name))
