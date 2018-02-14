#!/usr/bin/python3

import configparser
import os.path
import os


def _get_specific_context(context_config, context_name):
    if context_config:
        if context_name:
            if not context_config.has_section(context_name):
                raise Exception(
                    "Context {} doesn't exist".format(context_name))
            else:
                return context_config[context_name]
        else:
            return context_config.defaults()
    else:
        return None


_ex_values = {
    "dp_build_dir":
        lambda state:
            "{}/{}".format(state["build_dir"],
                           state["section"]),
    "dp_src_dir":
        lambda state:
            "{}/{}".format(state["src_dir"],
                           state["section"])
}


def _add_section_values(config, state_variables):
    for key, fn in _ex_values.items():
        config[key] = fn(state_variables)


def _add_context_values(config, context_config):
    for key, value in context_config.items():
        if key not in config:
            config[key] = value


def write_cache(build_config, context_config, build_dir,
                context_name=None, cache_name="build.cache"):
    context_section = _get_specific_context(context_config, context_name)
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    state_variables = {
        "src_dir": os.getcwd()
    }
    if os.path.isabs(build_dir):
        state_variables["build_dir"] = build_dir
    else:
        state_variables["build_dir"] = "{}/{}".format(os.getcwd(), build_dir)

    for section in build_config.sections():
        state_variables["section"] = section
        _add_section_values(build_config[section], state_variables)

    _add_context_values(build_config.defaults(), context_section)
    with open("{}/{}".format(build_dir, cache_name), 'w') as output_file:
        build_config.write(output_file)
