#!/usr/bin/python3

import configparser
import os
import os.path


def read_config(path):
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    config.read(path)

    return config




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
        config = transform_config(read_config(input_path), {
            "build_dir": cache_dir,
            "src_dir": os.path.abspath(os.path.dirname(input_path))
        }, context)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        with open(output, 'w') as output_file:
            config.write(output_file)
        # seems like we need to reload the cache file to get interpolation :(
        return read_config(output)
    else:
        return read_config(output)
