#!/usr/bin/python3

import subprocess

import devpipeline.common


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
        subprocess.check_call(install_args)


_usable_args = {
    "args": lambda v: [x.strip() for x in v.split(",")],
    "prefix": lambda v: ["-DCMAKE_INSTALL_PREFIX={}".format(v)],
    "cc": lambda v: ["-DCMAKE_C_COMPILER={}".format(v)],
    "cxx": lambda v: ["-DCMAKE_CXX_COMPILER={}".format(v)],
    "toolchain_file": lambda v: ["-DCMAKE_TOOLCHAIN_FILE={}".format(v)]
}


def make_cmake(component):
    cmake_args = []
    devpipeline.common.args_builder("cmake", component, _usable_args,
                                    lambda v, fn: cmake_args.extend(fn(v)))
    return CMake(cmake_args)
