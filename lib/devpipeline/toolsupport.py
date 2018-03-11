#!/usr/bin/python3

import re

import devpipeline.config.modifier


class SimpleTool():
    def __init__(self, executor, name, env, real):
        self.env = env
        self.executor = executor
        self.name = name
        self.real = real
        # print("executor={}".format(executor))
        # print("name={}".format(name))
        # print("env={}".format(env))
        # print("real={}".format(real))

    def _call_helper(self, step, fn, *fn_args):
        common_tool_helper(
            self.executor, step, self.env,
            self.name, fn, *fn_args)


def tool_builder(component, key, tool_map, *args):
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


def args_builder(prefix, component, args_dict, value_found_fn):
    for key, fn in args_dict.items():
        option = "{}.{}".format(prefix, key)
        value = devpipeline.config.modifier.modify_everything(component.get(option), component, option, ",")
        value_found_fn(value, fn)


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


def common_tool_helper(executor, step, env, name, fn, *fn_args):
    executor.message("{} {}".format(step, name))
    cmds = fn(*fn_args)
    if cmds:
        executor.execute(env, *cmds)
    else:
        executor.message("\t(Nothing to do)")
