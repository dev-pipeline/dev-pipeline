#!/usr/bin/python3

import pkg_resources


def query_plugins(entry_point_name):
    entries = {}
    for entry_point in pkg_resources.iter_entry_points(entry_point_name):
        entries[entry_point.name] = entry_point.load()
    return entries
