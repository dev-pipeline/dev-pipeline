#!/usr/bin/python3

import os.path

import devpipeline.config.parser
import devpipeline.config.paths


def read_all_profiles(base_dir, profile_list, fn):
    path = devpipeline.config.paths.get_profile_path(base_dir)
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
