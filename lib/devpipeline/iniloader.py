#!/usr/bin/python3

import configparser
import os
import os.path
import re

import devpipeline.component


def _read_config(path):
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    config.read(path)

    return config


def transform_config(config, state):
    transform_patterns = {
        R"\[\[dp_build_dir\]\]":
            lambda m, state:
                "{}/{}/{}".format(os.getcwd(),
                                  state["build_dir"],
                                  state["section"])
    }

    def alter_values(raw_value):
        ret = raw_value
        for pattern, repl in transform_patterns.items():
            ret = re.sub(pattern, lambda m: repl(m, state), ret)
        return ret

    ret = configparser.ConfigParser()
    for s in config.sections():
        ret.add_section(s)
        state["section"] = s
        for key, value in config.items(s, raw=True):
            ret[s][key] = alter_values(value)
    return ret


def build_cache(input, output, force=False):
    force = force or not os.path.isfile(output)
    if force or os.path.getmtime(input) > os.path.getmtime(output):
        cache_dir = os.path.dirname(output)
        config = transform_config(_read_config(input), {
            "build_dir": cache_dir
        })
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        with open(output, 'w') as output_file:
            config.write(output_file)
        # seems like we need to reload the cache file to get interpolation :(
        return _read_config(output)
    else:
        return _read_config(output)


def read_config(input, cache_dir, cache_file):
    config = build_cache(input, "{}/{}".format(cache_dir, cache_file))
    ret = devpipeline.component.Components()
    for name in config.sections():
        comp = devpipeline.component.Component(name)
        for key in config[name]:
            comp.add_value(key, config[name][key])
        ret.add(comp)

    return ret
