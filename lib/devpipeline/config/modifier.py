#!/usr/bin/python3

import re

import devpipeline.config.config
import devpipeline.config.parser
import devpipeline.config.paths
import devpipeline.config.profile

def _prepend(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(new_value, separator, old_value)
    else:
        return new_value


def _append(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(old_value, separator, new_value)
    else:
        return new_value


def _set(separator, old_value, new_value):
    return new_value


def _delete(separator, old_value, new_value):
    return None


_modifiers = {
    "prepend": _prepend,
    "append": _append,
    "override": _set,
    "erase": _delete
}


_modifier_order = [
    "prepend",
    "append",
    "override",
    "erase"
]


def modify(value, config, key, separator):
    for modifier in _modifier_order:
        mod_key = "{}.{}".format(key, modifier)
        if mod_key in config:
            try:
                value = _modifiers[modifier](separator, value, config.get(mod_key))
            except Exception as e:
                pass
    return value


def _apply_profiles(value, config, key, separator):
    def _apply_values(profile_name, profile_config):
        nonlocal value
        value = modify(value, profile_config, key, separator)

    profile_list = config.get("dp.profile_name")
    if profile_list:
        devpipeline.config.profile.read_all_profiles(
            devpipeline.config.paths.get_profile_path(),
            devpipeline.config.config.split_list(profile_list),
            _apply_values)
    return value


_modify_functions = [
    _apply_profiles
]


def modify_everything(value, config, key, separator):
    value = modify(value, config, key, separator)
    for modifier in _modify_functions:
        value = modifier(value, config, key, separator)
    return value
