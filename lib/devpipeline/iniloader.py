#!/usr/bin/python3

import configparser
import os
import os.path

import devpipeline.component


def _read_config(path):
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    config.read(path)

    return config


_ex_values = {
    "dp_build_dir":
        lambda state:
            "{}/{}/{}".format(os.getcwd(),
                              state["build_dir"],
                              state["section"]),
    "dp_src_dir":
        lambda state:
            "{}/{}".format(state["src_dir"],
                           state["section"])
}


def transform_config(config, state, context):
    ret = configparser.ConfigParser()
    for s in config.sections():
        ret.add_section(s)
        state["section"] = s
        for key, value in config.items(s, raw=True):
            ret[s][key] = value
        for ex, fn in _ex_values.items():
            ret[s][ex] = fn(state)

    # Add any context variables
    if context:
        for key, value in context._values.items():
            ret["DEFAULT"][key] = value
    return ret


def build_cache(input_path, output, context, force=False):
    force = force or not os.path.isfile(output)
    if force or os.path.getmtime(input_path) > os.path.getmtime(output):
        cache_dir = os.path.dirname(output)
        config = transform_config(_read_config(input_path), {
            "build_dir": cache_dir,
            "src_dir": os.path.abspath(os.path.dirname(input_path))
        }, context)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        with open(output, 'w') as output_file:
            config.write(output_file)
        # seems like we need to reload the cache file to get interpolation :(
        return _read_config(output)
    else:
        return _read_config(output)


def read_config(input_path, cache_path=None, context=None):
    if cache_path:
        config = build_cache(input_path, cache_path, context)
    else:
        config = _read_config(input_path)
    ret = devpipeline.component.Components()
    for name in config.sections():
        comp = devpipeline.component.Component(name)
        for key in config[name]:
            comp.add_value(key, config[name][key])
        ret.add(comp)

    return ret
