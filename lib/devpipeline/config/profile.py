#!/usr/bin/python3

"""Manage configuration related to profiles."""

import os.path

import devpipeline.config.parser
import devpipeline.config.paths


def apply_all_profiles(profile_config, profile_list, found_fn):
    """
    Apply a set of profiles.

    Arguments
    profile_config - The configuration for all available profiles.
    profile_list - A list of profiles that should be applied.
    found_fn - The function to call for each profile in profile_list.
               found_fn takes two parameters: the name of the profile being
               passed, and that profile's configuration.
    """
    count = 0
    for profile in profile_list:
        if profile_config.has_section(profile):
            found_fn(profile, profile_config[profile])
            count += 1
        else:
            print("Warning: profile '{}' not in configuration".format(profile))
    return count


def read_profiles(path):
    """
    Read requested profiles.

    Arguments
    path -- a path to a profile configuration
    profile_list -- a list of profiles to query
    found_fn -- the function to call for every found profile
    """
    if os.path.isfile(path):
        return devpipeline.config.parser.read_config(path)
    raise Exception("Unable to load profile file ({})".format(path))


def apply_profiles(target_config, config_map, found_fn):
    """
    Apply profiles values during option modification.

    Arguments
    config -- a package configuration
    found_fn -- a function to call after loading a profile
    """
    profile_list = target_config.get("dp.profile_name")
    if profile_list:
        if "profile_config" not in config_map:
            config_map["profile_config"] = read_profiles(
                devpipeline.config.paths.get_profile_path(config_map=config_map))
        apply_all_profiles(config_map["profile_config"],
                           devpipeline.config.config.split_list(profile_list),
                           found_fn)
