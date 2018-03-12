#!/usr/bin/python3

import os.path

import devpipeline.config.parser
import devpipeline.config.paths


def read_all_profiles(path, profile_list, fn):
    count = 0
    if os.path.isfile(path):
        parser = devpipeline.config.parser.read_config(path)
        for profile in profile_list:
            if parser.has_section(profile):
                fn(profile, parser[profile])
                count += 1
            else:
                print("Warning: profile '{}' not in configuration '{}'".format(
                    profile, path))
    return count


def apply_profiles(config, key, fn):
    profile_list = config.get("dp.profile_name")
    if profile_list:
        read_all_profiles(
            devpipeline.config.paths.get_profile_path(),
            devpipeline.config.config.split_list(profile_list), fn)