#!/usr/bin/python3

import os.path
import os

import devpipeline.config.parser


def _is_cache_dir_appropriate(cache_dir, cache_file):
    if os.path.exists(cache_dir):
        files = os.listdir(cache_dir)
        if cache_file in files:
            return True
        else:
            return not bool(files)
    else:
        return True


def _add_default_options(config, state):
    for key, value in state.items():
        config["DEFAULT"][key] = value


def _make_src_dir(config, package_name):
    src_path = None
    if "src_path" in config:
        src_path = config.get("src_path")
        if os.path.isabs(src_path):
            return src_path
    if not src_path:
        src_path = package_name
    return "{}/{}".format(config.get("dp.src_root"), src_path)


_package_options = {
    "dp.build_dir":
        lambda config, package_name:
            "{}/{}".format(config.get("dp.build_root"), package_name),
    "dp.src_dir": _make_src_dir
}


def _add_package_options(config, package_name, state):
    for key, fn in _package_options.items():
        config[key] = fn(config, package_name)


def _add_package_options_all(config, state):
    for package in config.sections():
        _add_package_options(config[package], package, state)


def create_cache(raw_path, cache_dir, cache_file):
    if _is_cache_dir_appropriate(cache_dir, cache_file):
        config = devpipeline.config.parser.read_config(raw_path)
        abs_path = os.path.abspath(raw_path)
        root_state = {
            "dp.build_root": "{}/{}".format(os.path.dirname(abs_path), cache_dir),
            "dp.src_root": os.path.dirname(abs_path)
        }
        _add_default_options(config, root_state)
        _add_package_options_all(config, root_state)
        with open("{}/{}".format(cache_dir, cache_file), 'w') as output_file:
            config.write(output_file)
        return config
    else:
        raise Exception(
            "{} doesn't look like a dev-pipeline folder".format(cache_dir))
