#!/usr/bin/python3

import os.path
import os

import devpipeline.config.parser
import devpipeline.version


def split_list(values, token=","):
    return [value.strip() for value in values.split(token)]


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


def _create_cache(raw_path, cache_dir, cache_file):
    if _is_cache_dir_appropriate(cache_dir, cache_file):
        config = devpipeline.config.parser.read_config(raw_path)
        abs_path = os.path.abspath(raw_path)
        root_state = {
            "dp.build_config": abs_path,
            "dp.src_root": os.path.dirname(abs_path),
            "dp.version": format(devpipeline.version.id, "02x")
        }
        if not os.path.isabs(cache_dir):
            root_state["dp.build_root"] = "{}/{}".format(os.path.dirname(abs_path), cache_dir)
        else:
            root_state["dp.build_root"] = cache_dir
        _add_default_options(config, root_state)
        _add_package_options_all(config, root_state)
        return config
    else:
        raise Exception(
            "{} doesn't look like a dev-pipeline folder".format(cache_dir))


def _write_config(config, cache_dir, cache_file):
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    with open("{}/{}".format(cache_dir, cache_file), 'w') as output_file:
        config.write(output_file)


def _set_list(config, kwargs_key, config_key, **kwargs):
    values = kwargs.get(kwargs_key)
    if values:
        config["DEFAULT"][config_key] = values


_config_modifiers = [
    lambda config, **kwargs:
        _set_list(config, "profiles", "dp.profile_name", **kwargs),
    lambda config, **kwargs:
        _set_list(config, "overrides", "dp.overrides", **kwargs)
]


def process_config(raw_path, cache_dir, cache_file, **kwargs):
    config = _create_cache(raw_path, cache_dir, cache_file)
    for modifier in _config_modifiers:
        modifier(config, **kwargs)
    _write_config(config, cache_dir, cache_file)
    return config


def find_config():
    previous = ""
    current = os.getcwd()
    while previous != current:
        check_path = "{}/build.cache".format(current)
        if os.path.isfile(check_path):
            return check_path
        else:
            previous = current
            current = os.path.dirname(current)
    raise Exception("Can't find build cache")


def _raw_updated(config, cache_mtime):
    raw_mtime = os.path.getmtime(config.get("DEFAULT", "dp.build_config"))
    return cache_mtime < raw_mtime


def _updated_software(config, cache_mtime):
    config_version = config.get("DEFAULT", "dp.version", fallback="0")
    return devpipeline.version.id > int(config_version, 16)


_outdated_checks = [
    _raw_updated,
    _updated_software
]


def _is_outdated(cache_file, cache_config):
    cache_mt = os.path.getmtime(cache_file)
    for check in _outdated_checks:
        if check(cache_config, cache_mt):
            return True
    return False


def update_cache(force=False):
    cache_file = find_config()
    cache_config = devpipeline.config.parser.read_config(cache_file)
    if force or _is_outdated(cache_file, cache_config):
        return (process_config(
            cache_config.get("DEFAULT", "dp.build_config"),
            os.path.dirname(cache_file), "build.cache",
            profiles=cache_config.get("DEFAULT", "dp.profile_name",
                                      fallback=None),
            overrides=cache_config.get("DEFAULT", "dp.overrides",
                                       fallback=None)), True)
    return (cache_config, False)
