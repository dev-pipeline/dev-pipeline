#!/usr/bin/python3
"""This modules supports building CMake projects."""

import re

import devpipeline.toolsupport


class CMake:

    """This class manages the details of building using CMake."""

    def __init__(self, ex_args, config_args):
        self.ex_args = ex_args
        self._config_args = config_args

    def configure(self, src_dir, build_dir):
        """This function builds the cmake configure command."""
        ex_path = self.ex_args.get("project_path")
        if ex_path:
            src_dir += "/{}".format(ex_path)

        return [{
            "args": [
                'cmake',
                src_dir,
            ] + self._config_args,
            "cwd": build_dir
        }]

    def build(self, build_dir):
        """This function builds the cmake build command."""
        # pylint: disable=no-self-use
        return [{
            "args": [
                'cmake',
                '--build',
                build_dir
            ]
        }]

    def install(self, build_dir, path=None):
        """This function builds the cmake install command."""
        # pylint: disable=no-self-use
        install_args = ['cmake',
                        '--build',
                        build_dir,
                        '--target',
                        'install']
        if path:
            install_args.extend(['--',
                                 "DESTDIR={}".format(path)])
        return [{
            "args": install_args
        }]


_all_cmake_args = None


def _handle_cmake_arg(value, fn):
    if value:
        return fn(value)
    else:
        return []


_usable_arg_fns = {
    "args": lambda v: _handle_cmake_arg(v, lambda v: [x.strip() for x in v.split(",")]),
    "prefix": lambda v: _handle_cmake_arg(v, lambda v: ["-DCMAKE_INSTALL_PREFIX={}".format(v)]),
    "cc": lambda v: _handle_cmake_arg(v, lambda v: ["-DCMAKE_C_COMPILER={}".format(v)]),
    "cxx": lambda v: _handle_cmake_arg(v, lambda v: ["-DCMAKE_CXX_COMPILER={}".format(v)]),
    "toolchain_file": lambda v: _handle_cmake_arg(v, lambda v: ["-DCMAKE_TOOLCHAIN_FILE={}".format(v)]),
    "build_type": lambda v: _handle_cmake_arg(v, lambda v: ["-DCMAKE_BUILD_TYPE={}".format(v)])
}

_usable_args = {
    "args": " ",
    "prefix": None,
    "cc": None,
    "cxx": None,
    "toolchain_file": None,
    "build_type": None
}

_valid_flag_suffixes = [
    "debug",
    "minsizerel",
    "release",
    "relwithdebinfo"
]


def _extend_flags_common(base_flags, suffix, value):
    if value:
        if suffix:
            base_flags += "_{}".format(suffix)
        return ["{}={}".format(base_flags, value)]
    else:
        return []


def _extend_cflags(base, suffix, value):
    return _extend_flags_common("-DCMAKE_{}_FLAGS".format(base),
                                suffix, value)


_cflag_args = [
    "cflags",
    "cxxflags"
]


def _make_common_args(arg_keys_list, prefix_string, suffix_string):
    new_args = devpipeline.toolsupport.build_flex_args_keys(
        [arg_keys_list, _valid_flag_suffixes])
    prefix_pattern = re.compile(prefix_string)
    suffix_pattern = re.compile(suffix_string)
    ret_args = {}
    ret_fns = {}
    for arg in new_args:
        prefix_match = prefix_pattern.search(arg)
        suffix_match = suffix_pattern.search(arg)
        ret_args[arg] = " "
        ret_fns[arg] = lambda v, pm=prefix_match, sm=suffix_match: _extend_cflags(
            pm.group(1).upper(), sm.group(1).upper(), v)
    for arg in arg_keys_list:
        prefix_match = prefix_pattern.search(arg)
        ret_args[arg] = " "
        ret_fns[arg] = lambda v, pm=prefix_match: _extend_cflags(
            pm.group(1).upper(), None, v)
    return (ret_args, ret_fns)


def _make_cflag_args():
    return _make_common_args(_cflag_args, R"(.*)flags", R"\.(\w+)$")


def _extend_ldflags(base, suffix, value):
    return _extend_flags_common("-DCMAKE_{}_LINKER_FLAGS".format(base),
                                suffix, value)


_ldflag_args = [
    "exe",
    "module",
    "shared",
    "static"
]


def _make_ldflag_args():
    base_args = devpipeline.toolsupport.build_flex_args_keys(
        [["ldflags"], _ldflag_args])
    return _make_common_args(base_args, R"ldflags\.(\w+)", R"\.(\w+)$")


_arg_builder_functions = [
    _make_cflag_args,
    _make_ldflag_args
]


def _make_all_options():
    global _all_cmake_args

    if not _all_cmake_args:
        cmake_args = _usable_args.copy()
        cmake_arg_fns = _usable_arg_fns.copy()
        for arg_builder in _arg_builder_functions:
            new_cmake_args, new_cmake_arg_fns = arg_builder()
            cmake_args.update(new_cmake_args)
            cmake_arg_fns.update(new_cmake_arg_fns)
        _all_cmake_args = (cmake_args, cmake_arg_fns)
    return _all_cmake_args


_ex_args = {
    "project_path": None
}

_ex_arg_fns = {
    "project_path": lambda v: ("project_path", v)
}


def make_cmake(current_target, common_wrapper):
    """This function initializes a CMake builder for building the project."""
    configure_args = []
    cmake_args = {}

    options, option_fns = _make_all_options()

    def add_value(v, key):
        k, r = _ex_arg_fns[key](v)
        cmake_args[k] = r

    devpipeline.toolsupport.args_builder("cmake", current_target, options,
                                         lambda v, key:
                                             configure_args.extend(option_fns[key](v)))
    devpipeline.toolsupport.args_builder("cmake", current_target, _ex_args,
                                         add_value)
    return common_wrapper(CMake(cmake_args, configure_args))
