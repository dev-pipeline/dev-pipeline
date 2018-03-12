#!/usr/bin/python3

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


def get_overrides_root(base_dir=None):
    return _make_path(base_dir, "overrides.d")


def get_profile_path(base_dir=None):
    return _make_path(base_dir, "profiles.conf")
