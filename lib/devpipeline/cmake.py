#!/usr/bin/python3

import subprocess


class CMake:
    def __init__(self, config_args, build_dir):
        self._config_args = config_args
        self._build_dir = build_dir

    def configure(self, src_dir):
        subprocess.check_call(['cmake',
                               src_dir,
                               ] + self._config_args,
                              cwd=self._build_dir)

    def build(self):
        subprocess.check_call(['cmake',
                               '--build',
                               self._build_dir])

    def install(self):
        subprocess.check_call(['cmake',
                               '--build',
                               self._build_dir,
                               '--target',
                               'install',
                               '--',
                               'DESTDIR=_install_'])


def make_cmake(component, build_dir):
    cmake_args = []
    if "cmake_args" in component._values:
        cmake_args.extend([x.strip()
                           for x in component._values["cmake_args"].split(",")])
    if "prefix" in component._values:
        cmake_args.append(
            "-DCMAKE_INSTALL_PREFIX={}".format(component._values["prefix"]))

    return CMake(cmake_args, build_dir)
