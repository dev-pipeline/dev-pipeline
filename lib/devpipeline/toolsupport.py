#!/usr/bin/python3
"""This module has tool helper classes and functions."""

import re

import devpipeline.config.modifier


class SimpleTool():

    """This class implements a simple tool for the dev-pipeline infrastructure."""
    # pylint: disable=too-few-public-methods

    def __init__(self, current_target, real):
        self.env = current_target["env"]
        self.executor = current_target["executor"]
        self.name = current_target["current_target"]
        self.real = real

    def _call_helper(self, step, helper_fn, *fn_args):
        common_tool_helper(
            self.executor, step, self.env,
            self.name, helper_fn, *fn_args)


def tool_builder(component, key, tool_map, *args):
    """This helper function initializes a tool with the given args."""
    # pylint: disable=protected-access
    tool_name = component.get(key)
    if tool_name:
        tool_fn = tool_map.get(tool_name)
        if tool_fn:
            return tool_fn(*args)
        else:
            raise Exception(
                "Unknown {} '{}' for {}".format(key, tool_name, component._name))
    else:
        raise Exception("{} does not specify {}".format(component._name, key))


def args_builder(prefix, current_target, args_dict, value_found_fn):
    for key, separator in args_dict.items():
        option = "{}.{}".format(prefix, key)
        value = devpipeline.config.modifier.modify_everything(
            current_target["current_config"].get(option), current_target, option, separator)
        value_found_fn(value, key)


def build_flex_args_keys(components):
    if len(components) > 1:
        sub_components = build_flex_args_keys(components[1:])
        ret = []
        for first in components[0]:
            for sub_component in sub_components:
                ret.append("{}.{}".format(first, sub_component))
        return ret
    elif len(components) == 1:
        return components[0]
    else:
        return []


def common_tool_helper(executor, step, env, name, helper_fn, *fn_args):
    # pylint: disable=missing-docstring
    executor.message("{} {}".format(step, name))
    cmds = helper_fn(*fn_args)
    if cmds:
        executor.execute(env, *cmds)
    else:
        executor.message("\t(Nothing to do)")
