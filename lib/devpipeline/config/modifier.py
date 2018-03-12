#!/usr/bin/python3

import re

import devpipeline.config.config
import devpipeline.config.override
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


def _apply_profiles(value, current_target, key, separator):
    def _apply_values(profile_name, profile_config):
        nonlocal value
        value = modify(value, profile_config, key, separator)

    devpipeline.config.profile.apply_profiles(current_target["current_config"], key, _apply_values)
    return value


def _apply_overrides(value, current_target, key, separator):
    def _apply_values(overrides, values):
        nonlocal value
        value = modify(value, values, key, separator)

    devpipeline.config.override.apply_overrides(current_target["current_config"], current_target["current_target"], _apply_values)
    return value


_modify_functions = [
    _apply_profiles,
    _apply_overrides
]


def modify_everything(value, current_target, key, separator):
    value = modify(value, current_target["current_config"], key, separator)
    for modifier in _modify_functions:
        value = modifier(value, current_target, key, separator)
    return value
