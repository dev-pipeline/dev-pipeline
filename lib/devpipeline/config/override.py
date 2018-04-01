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


def read_override(config):
    ret = {}
    for section in config.sections():
        suffix = _OVERRIDE_VALUES.get(section)
        if suffix:
            _add_override_values(config[section], suffix, ret)
        else:
            print("Warning: override has unknown section '{}'".
                  format(section), file=sys.stderr)
    return ret


def apply_all_overrides(override_configs, found_fn):
    count = 0
    for override, config in override_configs:
        values = read_override(config)
        if values:
            found_fn(override, values)
            count += 1
    return count


def read_overrides(base_dir, name, override_list):
    ret = []
    for override in override_list:
        path = "{}/{}/{}.conf".format(base_dir, override, name)
        if os.path.isfile(path):
            ret.append((override,
                        devpipeline.config.parser.read_config(path)))
    return ret


def apply_overrides(config, name, config_map, found_fn):
    override_list = config.get("dp.overrides")
    if override_list:
        split_list = devpipeline.config.config.split_list(override_list)
        if "overrides" not in config_map[name]:
            config_map[name]["overrides"] = read_overrides(
                devpipeline.config.paths.get_overrides_root(
                    config_map=config_map),
                name, split_list)
        apply_all_overrides(config_map[name]["overrides"], found_fn)
