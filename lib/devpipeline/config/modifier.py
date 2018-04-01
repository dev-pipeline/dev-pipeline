#!/usr/bin/python3

"""Support modification of option values."""

import devpipeline.config.config
import devpipeline.config.override
import devpipeline.config.parser
import devpipeline.config.paths
import devpipeline.config.profile


def _prepend(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(new_value, separator, old_value)
    return new_value


def _append(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(old_value, separator, new_value)
    return new_value


def _set(separator, old_value, new_value):
    # pylint: disable=unused-argument
    return new_value


def _delete(separator, old_value, new_value):
    # pylint: disable=unused-argument
    return None


_MODIFIERS = {
    "prepend": _prepend,
    "append": _append,
    "override": _set,
    "erase": _delete
}


_MODIFIER_ORDER = [
    "prepend",
    "append",
    "override",
    "erase"
]


def modify(value, config, key, separator):
    """
    Modify a value based on configuration alterations.

    Arguments
    value -- the initial value
    config -- a dictionary-like object to query for modifiers
    key -- the base to use for modifier options
    separator -- a value to use for concatination alterations
    """
    for modifier in _MODIFIER_ORDER:
        mod_key = "{}.{}".format(key, modifier)
        if mod_key in config:
            value = _MODIFIERS[modifier](
                separator, value, config.get(mod_key))
    return value


def _apply_profiles(value, current_target, key, separator):
    def _apply_values(profile_name, profile_config):
        # pylint: disable=unused-argument
        nonlocal value
        value = modify(value, profile_config, key, separator)

    devpipeline.config.profile.apply_profiles(
        current_target["current_config"], current_target, _apply_values)
    return value


def _apply_overrides(value, current_target, key, separator):
    def _apply_values(overrides, values):
        # pylint: disable=unused-argument
        nonlocal value
        value = modify(value, values, key, separator)

    devpipeline.config.override.apply_overrides(
        current_target["current_config"],
        current_target["current_target"],
        current_target, _apply_values)
    return value


_MODIFY_FUNCTIONS = [
    _apply_profiles,
    _apply_overrides
]


def modify_everything(value, current_target, key, separator):
    """
    Modify a value using all possible modifiers.

    The available modifiers will depend on a project configuration.

    Arguments
    value -- the initial value
    current_target -- information about the currrent target being processed
    key -- the option being modified
    separator -- a value to use for any alterations that require concatination
    """
    value = modify(value, current_target["current_config"], key, separator)
    for modifier in _MODIFY_FUNCTIONS:
        value = modifier(value, current_target, key, separator)
    return value
