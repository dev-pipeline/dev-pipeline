#!/usr/bin/python3

"""Functionality related to override files"""

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


def _build_override(config):
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
    """
    Pass available overrides to a caller.

    This function will return the number of overrides with values.

    Arguments
    override_configs - A list of override names and configurations.
    found_fn - A function to pass available override information.  found_fn
               should take two arguments: the name of an override, and the
               configuration.
    """
    count = 0
    for override, config in override_configs:
        values = _build_override(config)
        if values:
            found_fn(override, values)
            count += 1
    return count


def read_overrides(base_dir, name, override_list):
    """
    Read any available override files.

    Arguments
    base_dir - The base directory for override configurations.
    name - The name of the target.
    override_list - The list of overrides to consider.
    """
    ret = []
    for override in override_list:
        path = devpipeline.config.paths.get_override_path(base_dir, override,
                                                          name)
        if os.path.isfile(path):
            ret.append((override,
                        devpipeline.config.parser.read_config(path)))
    return ret


def apply_overrides(config, name, config_map, found_fn):
    """
    Apply all available overrides.

    Arguments
    config - The configuration for some target.
    name - The target having overrides applied.
    config_map - A configuration map.  If the overrides haven't been loaded
                 yet, they'll be stored in this map.
    found_fn - A function to call when an override has been loaded.  It should
               take two arguments: the name of the loaded override, and the
               values provided by that override.
    """
    override_list = config.get("dp.overrides")
    if override_list:
        split_list = devpipeline.config.config.split_list(override_list)
        if "overrides" not in config_map[name]:
            config_map[name]["overrides"] = read_overrides(
                devpipeline.config.paths.get_overrides_root(
                    config_map=config_map),
                name, split_list)
        apply_all_overrides(config_map[name]["overrides"], found_fn)
