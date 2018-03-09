#!/usr/bin/python3

import os.path
import sys

import devpipeline.config.parser
import devpipeline.config.paths


def _add_override_values(config, section, suffix, values):
    for key, value in config.items():
        values["{}.{}".format(key, suffix)] = value


_override_values = {
    "append": "append",
    "prepend": "prepend",
    "override": "override",
    "erase": "erase"
}


def read_override(path):
    ret = {}
    if os.path.isfile(path):
        parser = devpipeline.config.parser.read_config(path)
        for section in parser.sections():
            suffix = _override_values.get(section)
            if suffix:
                _add_override_values(parser[section], section, suffix, ret)
            else:
                print("Warning: override file {} has unknown section '{}'".
                      format(path, section), file=sys.stderr)
    return ret


def read_all_overrides(base_dir, override_list, package, fn):
    count = 0
    for override in override_list:
        path = "{}/{}/{}.conf".format(
            devpipeline.config.paths.get_overrides_root(base_dir),
            override, package)
        values = read_override(path)
        if values:
            fn(override, values)
            count += 1
    return count
