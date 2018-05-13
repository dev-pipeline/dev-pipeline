#!/usr/bin/python3

"""A module to manage configuring a project."""

import os.path
import os

import devpipeline.config.parser
import devpipeline.version


def split_list(values, split_string=","):
    """
    Convert a delimited string to a list.

    Arguments
    values -- a string to split
    split_string -- the token to use for splitting values
    """
    return [value.strip() for value in values.split(split_string)]


def _is_cache_dir_appropriate(cache_dir, cache_file):
    """
    Determine if a directory is acceptable for building.

    A directory is suitable if any of the following are true:
      - it doesn't exist
      - it is empty
      - it contains an existing build cache
    """
    if os.path.exists(cache_dir):
        files = os.listdir(cache_dir)
        if cache_file in files:
            return True
        return not bool(files)
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


_PACKAGE_OPTIONS = {
    "dp.build_dir": lambda config, package_name: "{}/{}".format(
        config.get("dp.build_root"), package_name),
    "dp.src_dir": _make_src_dir
}


def _add_package_options(config, package_name, state):
    # pylint: disable=unused-argument
    for key, option_fn in _PACKAGE_OPTIONS.items():
        config[key] = option_fn(config, package_name)


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
            "dp.version": format(devpipeline.version.ID, "02x")
        }
        if not os.path.isabs(cache_dir):
            root_state["dp.build_root"] = "{}/{}".format(
                os.path.dirname(abs_path), cache_dir)
        else:
            root_state["dp.build_root"] = cache_dir
        _add_default_options(config, root_state)
        _add_package_options_all(config, root_state)
        return config
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


_CONFIG_MODIFIERS = [
    lambda config, **kwargs: _set_list(config, "profiles",
                                       "dp.profile_name", **kwargs),
    lambda config, **kwargs: _set_list(config, "overrides",
                                       "dp.overrides", **kwargs)
]


def process_config(raw_path, cache_dir, cache_file, **kwargs):
    """
    Read a build configuration and create it, storing the result in a build
    cache.

    Arguments
    raw_path -- path to a build configuration
    cache_dir -- the directory where cache should be written
    cache_file -- The filename to write the cache.  This will live inside
                  cache_dir.
    **kwargs -- additional arguments used by some modifiers
    """
    config = _create_cache(raw_path, cache_dir, cache_file)
    for modifier in _CONFIG_MODIFIERS:
        modifier(config, **kwargs)
    _write_config(config, cache_dir, cache_file)
    return config


def find_config():
    """Find a build cache somewhere in a parent directory."""
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
    # pylint: disable=unused-argument
    config_version = config.get("DEFAULT", "dp.version", fallback="0")
    return devpipeline.version.ID > int(config_version, 16)


_OUTDATED_CHECKS = [
    _raw_updated,
    _updated_software
]


def _is_outdated(cache_file, cache_config):
    cache_mt = os.path.getmtime(cache_file)
    for check in _OUTDATED_CHECKS:
        if check(cache_config, cache_mt):
            return True
    return False


def update_cache(force=False, cache_file=None):
    """
    Load a build cache, updating it if necessary.

    A cache is considered outdated if any of its inputs have changed.

    Arguments
    force -- Consider a cache outdated regardless of whether its inputs have
             been modified.
    """
    if not cache_file:
        cache_file = find_config()
    cache_config = devpipeline.config.parser.read_config(cache_file)
    if force or _is_outdated(cache_file, cache_config):
        cache_config = process_config(
            cache_config.get("DEFAULT", "dp.build_config"),
            os.path.dirname(cache_file), "build.cache",
            profiles=cache_config.get("DEFAULT", "dp.profile_name",
                                      fallback=None),
            overrides=cache_config.get("DEFAULT", "dp.overrides",
                                       fallback=None))
    return cache_config
