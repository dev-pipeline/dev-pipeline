#!/usr/bin/python3

"""Functions related to configuration paths"""

import os.path

_DEFAULT_PATH = "{}/.dev-pipeline.d".format(os.path.expanduser("~"))


def _get_config_dir():
    env_override = os.environ.get("DEV_PIPELINE_CONFIG")
    if env_override:
        return env_override
    return _DEFAULT_PATH


def _make_path(base_dir, ending):
    if not base_dir:
        base_dir = _get_config_dir()
    return "{}/{}".format(base_dir, ending)


def _override_base_dir(config_map):
    if "config_dir" in config_map:
        return config_map["config_dir"]
    return None


def get_overrides_root(base_dir=None, config_map=None):
    """
    Get the root path for override files.

    Arguments
    base_dir - The base directory to search in.
    config_map - A configuration map.  If provided, this will override
                 base_dir.
    """
    if config_map:
        base_dir = _override_base_dir(config_map)
    return _make_path(base_dir, "overrides.d")


def get_override_path(base_dir, override_name, package_name):
    """
    Get the path of a specific override file.

    Override files are organized by the override name and the package name.

    Arguments
    base_dir - The root directory where override configurations are stored.
    override_name - The name of the override being considered.
    package_name - The package being considered.
    """
    return "{}/{}/{}.conf".format(base_dir, override_name, package_name)


def get_profile_path(base_dir=None, config_map=None):
    """
    Get the path to the profile configuration.

    Arguments
    base_dir - The base directory for configuration.
    config_map - A configuration map.  If provided, this will override any
                 value in base_dir.
    """
    if config_map:
        base_dir = _override_base_dir(config_map)
    return _make_path(base_dir, "profiles.conf")
