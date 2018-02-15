#!/usr/bin/python3

import configparser
import os.path
import os


class ConfigFinder:
    def __init__(self, filename):
        self.filename = filename

    def read_config(self):
        config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
        config.read(self.filename)

        return config


_context_file = "{}/{}".format(os.path.expanduser("~"), ".dev-pipeline")


class ContextConfig:
    def __init__(self, context_name=None):
        self.name = context_name

    def _get_specific_context(self, context_config):
        if self.name:
            if not context_config.has_section(self.name):
                raise Exception(
                    "Context {} doesn't exist".format(self.name))
            else:
                return context_config[self.name]
        else:
            return context_config.defaults()

    def read_config(self):
        if os.path.isfile(_context_file):
            return self._get_specific_context(
                ConfigFinder(_context_file).read_config())


def _add_root_values(config, state_variables):
    defaults = config.defaults()
    defaults["dp.build_root"] = state_variables["build_dir"]
    defaults["dp.src_root"] = state_variables["src_dir"]


_ex_values = {
    "dp.build_dir":
        lambda state:
            "${{dp.build_root}}/{}".format(state["section"]),
    "dp.src_dir":
        lambda state:
            "${{dp.src_root}}{}".format(state["section"])
}


def _add_section_values(config, state_variables):
    for section in config.sections():
        state_variables["section"] = section
        for key, fn in _ex_values.items():
            config[section][key] = fn(state_variables)


def _add_default_values(config, state_variables):
    for key, value in state_variables.items():
        config[key] = value


def _add_context_values(config, context_config):
    for key, value in context_config.items():
        if key not in config:
            config[key] = value


def write_cache(config_reader, context_config_reader, build_dir,
                cache_name="build.cache"):
    config = config_reader.read_config()
    context_section = context_config_reader.read_config()
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    state_variables = {
        "src_dir": os.path.dirname(os.path.abspath(config_reader.filename))
    }
    if os.path.isabs(build_dir):
        state_variables["build_dir"] = build_dir
    else:
        state_variables["build_dir"] = "{}/{}".format(os.getcwd(), build_dir)

    _add_section_values(config, state_variables)
    _add_context_values(config.defaults(), context_section)
    _add_default_values(config.defaults(), {
        "dp.build_root": state_variables["build_dir"],
        "dp.src_root": state_variables["src_dir"]
    })
    with open("{}/{}".format(build_dir, cache_name), 'w') as output_file:
        config.write(output_file)
