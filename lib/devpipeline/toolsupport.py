#!/usr/bin/python3

import re


def tool_builder(component, key, tool_map):
    tool_name = component.get(key)
    if tool_name:
        tool_fn = tool_map.get(tool_name)
        if tool_fn:
            return tool_fn(component)
        else:
            raise Exception(
                "Unknown {} '{}' for {}".format(key, tool_name, component._name))
    else:
        raise Exception("{} does not specify {}".format(component._name, key))


def args_builder(prefix, component, args_dict, val_found_fn):
    pattern = re.compile(R"^{}\.".format(prefix))
    for key, value in component.items():
        m = pattern.match(key)
        if m:
            real_key = key[m.end():]
            hit = args_dict.get(real_key)
            if hit:
                val_found_fn(value, hit)


def flex_args_builder(prefix, component, args_dict, val_found_fn):
    for key, flex_fn in args_dict.items():
        pattern = re.compile(R"^{}\.({})\.?".format(prefix, key))
        for option, value in component.items():
            m = pattern.match(option)
            if m:
                val_found_fn(value, option[m.end():], flex_fn)
