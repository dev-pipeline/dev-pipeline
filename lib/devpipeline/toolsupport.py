#!/usr/bin/python3
"""This module has tool helper classes and functions."""

import devpipeline.config.modifier


class SimpleTool():
    """
    This class implements a simple tool for the dev-pipeline infrastructure.
    It handles setting the environment and working with an executor so clients
    only have to worry about the arguments to the subprocess module.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, current_target, real):
        self.env = current_target["env"]
        self.executor = current_target["executor"]
        self.name = current_target["current_target"]
        self.real = real

    def _call_helper(self, step, helper_fn, *fn_args):
        self.executor.message("{} {}".format(step, self.name))
        cmds = helper_fn(*fn_args)
        if cmds:
            self.executor.execute(self.env, *cmds)
        else:
            self.executor.message("\t(Nothing to do)")


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
                "Unknown {} '{}' for {}".format(
                    key, tool_name, component._name))
    else:
        raise Exception("{} does not specify {}".format(component._name, key))


def args_builder(prefix, current_target, args_dict, value_found_fn):
    """
    Process arguments a tool cares about.

    Since most tools require configuration, this function helps deal with the
    boilerplate.  Each option will be processed based on all modifications
    supported by dev-pipeline (i.e., profiles and overrides) in the proper
    order.

    Arguments:
    prefix -- The prefix for each argument.  This will be applied to
              everything in args_dict.
    current_target -- Information about the current target being processed.
    args_dict -- Something that acts like a dictionary.  The keys should be
                 options to deal with and the value should be the separtor
                 value the option requires.
    value_found_fn -- A function to call when a match is found.
    """
    for key, separator in args_dict.items():
        option = "{}.{}".format(prefix, key)
        value = devpipeline.config.modifier.modify_everything(
            current_target["current_config"].get(option), current_target, option, separator)
        value_found_fn(value, key)


def build_flex_args_keys(components):
    """
    Helper function to build a list of options.

    Some tools require require variations of the same options (e.g., cflags
    for debug vs release builds), but manually creating those options is
    cumbersome and error-prone.  This function handles that work by combining
    all possible comintations of the values in components.

    Arguments
    components -- A list of lists that should be combined to form options.
    """
    def _prepend_first(components, sub_components):
        ret = []
        for first in components[0]:
            for sub_component in sub_components:
                ret.append("{}.{}".format(first, sub_component))
        return ret

    if len(components) > 1:
        sub_components = build_flex_args_keys(components[1:])
        return _prepend_first(components, sub_components)
    elif len(components) == 1:
        return components[0]
    return []
