#!/usr/bin/python3

"""Functionality related to environment configuration"""

import os
import re

import devpipeline.config.modifier
import devpipeline.config.override
import devpipeline.config.profile

_ENV_PATTERN = re.compile(R"env.(\w+)")


def _add_override(values, adjustments):
    for key in values:
        match = _ENV_PATTERN.match(key)
        if match:
            adjustments[match.group(1)] = None


def _source_config(config_map, adjustments):
    _add_override(config_map["current_config"], adjustments)


def _source_profiles(config_map, adjustments):
    def _add_override_helper(profile_name, profile_config):
        # pylint: disable=unused-argument
        _add_override(profile_config, adjustments)

    devpipeline.config.profile.apply_profiles(
        config_map["current_config"],
        config_map, _add_override_helper)


def _source_overrides(config_map, adjustments):
    def _add_override_helper(overrides, values):
        # pylint: disable=unused-argument
        _add_override(values, adjustments)

    devpipeline.config.override.apply_overrides(
        config_map["current_config"],
        config_map["current_target"],
        config_map, _add_override_helper)


_SOURCE_FUNCTIONS = [
    _source_config,
    _source_profiles,
    _source_overrides
]


def get_env_list(config_map):
    """
    Retrieve a list of environemnt variables a configuration will modify.

    The list of variables will include anything in a configuration (including
    in extra configuration files) that can alter the environment.  The list
    will include only the variable names, not the env prefix.

    Arguments
    config_map - A configuration map.
    """
    env_adjustments = {}
    for source in _SOURCE_FUNCTIONS:
        source(config_map, env_adjustments)
    return env_adjustments.keys()


def create_environment(config_map):
    """
    Create a modified environment.

    Arguments
    config_map - A configuration map.
    """
    def _apply_override(adjustment, ret):
        upper_key = adjustment.upper()
        initial_value = config_map["current_config"].get(
            "env.{}".format(adjustment))
        if not initial_value:
            initial_value = ret.get(upper_key)
        new_value = devpipeline.config.modifier.modify_everything(
            initial_value, config_map,
            "env.{}".format(adjustment), os.pathsep)
        if new_value:
            ret[upper_key] = new_value
        else:
            ret.pop(upper_key, None)

    env_adjustments = get_env_list(config_map)
    if env_adjustments:
        ret = os.environ.copy()
        for adjustment in env_adjustments:
            _apply_override(adjustment, ret)
        return ret
    return os.environ
