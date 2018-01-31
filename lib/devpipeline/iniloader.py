#!/usr/bin/python3

import configparser

import devpipeline.component


def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)

    ret = devpipeline.component.Components()
    for name in config.sections():
        comp = devpipeline.component.Component(name)
        for key in config[name]:
            comp.add_value(key, config[name][key])
        ret.add(comp)

    return ret
