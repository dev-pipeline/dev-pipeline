#!/usr/bin/python3
"""This module has tool helper classes and functions."""

import re

class SimpleTool():
    """This class implements a simple tool for the dev-pipeline infrastructure."""
    # pylint: disable=too-few-public-methods
    def __init__(self, executor, name, env, real):
        self.env = env
        self.executor = executor
        self.name = name
        self.real = real
        # print("executor={}".format(executor))
        # print("name={}".format(name))
        # print("env={}".format(env))
        # print("real={}".format(real))

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
            return tool_fn(component, *args)
        else:
            raise Exception(
                "Unknown {} '{}' for {}".format(key, tool_name, component._name))
    else:
        raise Exception("{} does not specify {}".format(component._name, key))


def _args_helper(pattern, component, helper_fn):
    for key, value in component.items():
        matches = pattern.match(key)
        if matches:
            helper_fn(key, value, matches)


def args_builder(prefix, component, args_dict, val_found_fn):
    """This helper function puts an argument list together."""
    def call_fn(key, value, matches):
        # pylint: disable=missing-docstring
        real_key = key[matches.end():]
        hit = args_dict.get(real_key)
        if hit:
            val_found_fn(value, hit)

    pattern = re.compile(R"^{}\.".format(prefix))
    _args_helper(pattern, component, call_fn)


def flex_args_builder(prefix, component, args_dict, val_found_fn):
    # pylint: disable=missing-docstring
    for key, flex_fn in args_dict.items():
        pattern = re.compile(R"^{}\.({})\.?".format(prefix, key))
        _args_helper(pattern, component,
                     lambda k, v, m, helper=flex_fn:
                     val_found_fn(v, k[m.end():], helper))


def common_tool_helper(executor, step, env, name, helper_fn, *fn_args):
    # pylint: disable=missing-docstring
    executor.message("{} {}".format(step, name))
    cmds = helper_fn(*fn_args)
    if cmds:
        executor.execute(env, *cmds)
    else:
        executor.message("\t(Nothing to do)")
