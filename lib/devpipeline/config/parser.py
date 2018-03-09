#!/usr/bin/python3

import configparser


def _make_parser():
    return configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())


def read_config(path):
    parser = _make_parser()
    parser.read(path)
    return parser


def write_config(config, path):
    with open(path, 'w') as output_file:
        config.write(output_file)
