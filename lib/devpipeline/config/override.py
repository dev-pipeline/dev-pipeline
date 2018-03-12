#!/usr/bin/python3

import os.path
import sys

import devpipeline.config.parser
import devpipeline.config.paths


def _add_override_values(config, suffix, values):
    for key, value in config.items():
        values["{}.{}".format(key, suffix)] = value


_OVERRIDE_VALUES = {
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
            suffix = _OVERRIDE_VALUES.get(section)
            if suffix:
                _add_override_values(parser[section], suffix, ret)
            else:
                print("Warning: override file {} has unknown section '{}'".
                      format(path, section), file=sys.stderr)
    return ret


def read_all_overrides(base_dir, override_list, package, found_fn):
    count = 0
    for override in override_list:
        path = "{}/{}/{}.conf".format(base_dir, override, package)
        values = read_override(path)
        if values:
            found_fn(override, values)
            count += 1
    return count


def apply_overrides(config, name, found_fn):
    override_list = config.get("dp.overrides")
    if override_list:
        read_all_overrides(
            devpipeline.config.paths.get_overrides_root(),
            devpipeline.config.config.split_list(override_list),
            name, found_fn)
