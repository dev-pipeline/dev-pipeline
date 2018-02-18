#!/usr/bin/python3

import subprocess

import devpipeline.common


class CMake(devpipeline.build.Builder):
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
    "toolchain_file": lambda v: ["-DCMAKE_TOOLCHAIN_FILE={}".format(v)],
    "build_type": lambda v: ["-DCMAKE_BUILD_TYPE={}".format(v)],
}

_valid_cflag_suffixes = [
    "DEBUG",
    "RELEASE"
]


def _extend_cflags(base, suffix, value):
    base_flags = "-DCMAKE_{}_FLAGS".format(base)
    if suffix:
        suffix = suffix.upper()
        if suffix in _valid_cflag_suffixes:
            base_flags += "_{}".format(suffix)
        else:
            raise Exception("{} is an invalid modifier".format(suffix))
    return ["{}={}".format(base_flags, value)]


_flag_args = {
    "cflags": lambda v, suffix: _extend_cflags("C", suffix, v),
    "cxxflags": lambda v, suffix: _extend_cflags("CXX", suffix, v)
}


def make_cmake(component):
    cmake_args = []

    devpipeline.common.args_builder("cmake", component, _usable_args,
                                    lambda v, fn: cmake_args.extend(fn(v)))
    devpipeline.common.flex_args_builder("cmake", component, _flag_args,
                                         lambda v, suffix, fn:
                                             cmake_args.extend(fn(v, suffix)))
    return CMake(cmake_args)
