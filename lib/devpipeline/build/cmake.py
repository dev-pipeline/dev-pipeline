#!/usr/bin/python3

import subprocess


class CMake:
    def __init__(self, config_args):
        self._config_args = config_args

    def configure(self, src_dir, build_dir):
        subprocess.check_call(['cmake',
                               src_dir,
                               ] + self._config_args,
                              cwd=build_dir)

    def build(self, build_dir):
        subprocess.check_call(['cmake',
                               '--build',
                               build_dir])

    def install(self, build_dir, path=None):
        install_args = ['cmake',
                        '--build',
                        build_dir,
                        '--target',
                        'install']
        if path:
            install_args.extend(['--',
                                 "DESTDIR={}".format(path)])
        print(install_args)
        subprocess.check_call(install_args)


def make_cmake(component):
    cmake_args = []
    val = component._values.get("cmake_args")
    if val:
        cmake_args.extend([x.strip() for x in val.split(",")])
    val = component._values.get("prefix")
    if val:
        cmake_args.append("-DCMAKE_INSTALL_PREFIX={}".format(val))

    return CMake(cmake_args)
