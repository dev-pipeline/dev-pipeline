#!/usr/bin/python3

import re


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


def _args_helper(pattern, component, fn):
    for key, value in component.items():
        m = pattern.match(key)
        if m:
            fn(key, value, m)


def args_builder(prefix, component, args_dict, val_found_fn):
    def call_fn(key, value, m):
        real_key = key[m.end():]
        hit = args_dict.get(real_key)
        if hit:
            val_found_fn(value, hit)

    pattern = re.compile(R"^{}\.".format(prefix))
    _args_helper(pattern, component, call_fn)


def flex_args_builder(prefix, component, args_dict, val_found_fn):
    for key, flex_fn in args_dict.items():
        pattern = re.compile(R"^{}\.({})\.?".format(prefix, key))
        _args_helper(pattern, component,
                     lambda k, v, m:
                     val_found_fn(v, k[m.end():], flex_fn))


def common_tool_helper(executor, step, env, name, fn, *fn_args):
    executor.message("{} {}".format(step, name))
    cmds = fn(*fn_args)
    if cmds:
        executor.execute(env, *cmds)
    else:
        executor.message("\t(Nothing to do)")
