#!/usr/bin/python3

"""Manage configuration related to profiles."""

import os.path

import devpipeline.config.parser
import devpipeline.config.paths


def read_all_profiles(path, profile_list, found_fn):
    """
    Read requested profiles and provide option lists via found_fn.

    Arguments
    path -- a path to a profile configuration
    profile_list -- a list of profiles to query
    found_fn -- the function to call for every found profile
    """
    def _iterate_profiles(parser):
        count = 0
        for profile in profile_list:
            if parser.has_section(profile):
                found_fn(profile, parser[profile])
                count += 1
            else:
                print("Warning: profile '{}' not in configuration '{}'".format(
                    profile, path))
        return count

    if os.path.isfile(path):
        parser = devpipeline.config.parser.read_config(path)
        return _iterate_profiles(parser)
    return 0


def apply_profiles(config, found_fn):
    """
    Apply profiles values during option modification.

    Arguments
    config -- a package configuration
    found_fn -- a function to call after loading a profile
    """
    profile_list = config.get("dp.profile_name")
    if profile_list:
        read_all_profiles(
            devpipeline.config.paths.get_profile_path(),
            devpipeline.config.config.split_list(profile_list), found_fn)
