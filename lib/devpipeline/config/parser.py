#!/usr/bin/python3

"""Manage reading and writing configurations to disk."""

import configparser


def _make_parser():
    return configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())


def read_config(path):
    """
    Read a configuration from disk.

    Arguments
    path -- the loation to deserialize
    """
    parser = _make_parser()
    parser.read(path)
    return parser


def write_config(config, path):
    """
    Write a configuration file.

    Arguments
    config -- a configuration
    path -- the location to serialize config
    """
    with open(path, 'w') as output_file:
        config.write(output_file)
