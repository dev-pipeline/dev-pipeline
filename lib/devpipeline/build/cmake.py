#!/usr/bin/python3

import subprocess

import devpipeline.toolsupport


class CMake(devpipeline.build.Builder):
    def __init__(self, ex_args, config_args):
        self.ex_args = ex_args
        self._config_args = config_args

    def configure(self, src_dir, build_dir):
        ex_path = self.ex_args.get("project_path")
        if ex_path:
            src_dir += "/{}".format(ex_path)

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
    "MINSIZEREL",
    "RELEASE",
    "RELWITHDEBINFO"
]


def _extend_flags_common(base_flags, suffix, value):
    if suffix:
        suffix = suffix.upper()
        if suffix in _valid_cflag_suffixes:
            base_flags += "_{}".format(suffix)
        else:
            raise Exception("{} is an invalid modifier".format(suffix))
    return ["{}={}".format(base_flags, value)]


def _extend_cflags(base, suffix, value):
    return _extend_flags_common("-DCMAKE_{}_FLAGS".format(base),
                                suffix, value)


def _extend_ldflags(base, suffix, value):
    return _extend_flags_common("-DCMAKE_{}_LINKER_FLAGS".format(base),
                                suffix, value)


_flag_args = {
    "cflags": lambda v, suffix: _extend_cflags("C", suffix, v),
    "cxxflags": lambda v, suffix: _extend_cflags("CXX", suffix, v),
    "ldflags.exe": lambda v, suffix: _extend_ldflags("EXE", suffix, v),
    "ldflags.module": lambda v, suffix: _extend_ldflags("MODULE", suffix, v),
    "ldflags.shared": lambda v, suffix: _extend_ldflags("SHARED", suffix, v),
    "ldflags.static": lambda v, suffix: _extend_ldflags("STATIC", suffix, v)
}

_ex_args = {
    "project_path": lambda v: ("project_path", v)
}


def make_cmake(component):
    configure_args = []
    cmake_args = {}

    def add_value(v, fn):
        k, r = fn(v)
        cmake_args[k] = r

    devpipeline.toolsupport.args_builder("cmake", component, _usable_args,
                                         lambda v, fn:
                                             configure_args.extend(fn(v)))
    devpipeline.toolsupport.flex_args_builder("cmake", component, _flag_args,
                                              lambda v, suffix, fn:
                                                  configure_args.extend(
                                                      fn(v, suffix)))
    devpipeline.toolsupport.args_builder("cmake", component, _ex_args,
                                         add_value)
    return CMake(cmake_args, configure_args)
