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


_ALL_CMAKE_ARGS = None


def _handle_cmake_arg(value, valid_fn):
    if value:
        return valid_fn(value)
    return []


_USABLE_ARG_FNS = {
    "args": lambda v: _handle_cmake_arg(
        v, lambda v: [x.strip() for x in v.split(",")]),
    "prefix": lambda v: _handle_cmake_arg(
        v, lambda v: ["-DCMAKE_INSTALL_PREFIX={}".format(v)]),
    "cc": lambda v: _handle_cmake_arg(
        v, lambda v: ["-DCMAKE_C_COMPILER={}".format(v)]),
    "cxx": lambda v: _handle_cmake_arg(
        v, lambda v: ["-DCMAKE_CXX_COMPILER={}".format(v)]),
    "toolchain_file": lambda v: _handle_cmake_arg(
        v, lambda v: ["-DCMAKE_TOOLCHAIN_FILE={}".format(v)]),
    "build_type": lambda v: _handle_cmake_arg(
        v, lambda v: ["-DCMAKE_BUILD_TYPE={}".format(v)])
}

_USABLE_ARGS = {
    "args": " ",
    "prefix": None,
    "cc": None,
    "cxx": None,
    "toolchain_file": None,
    "build_type": None
}

_VALID_FLAG_SUFFIXES = [
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


def _make_common_args(arg_keys_list, prefix_string, suffix_string):
    new_args = devpipeline.toolsupport.build_flex_args_keys(
        [arg_keys_list, _VALID_FLAG_SUFFIXES])
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


_CFLAG_ARGS = [
    "cflags",
    "cxxflags"
]


def _make_cflag_args():
    return _make_common_args(_CFLAG_ARGS, R"(.*)flags", R"\.(\w+)$")


def _extend_ldflags(base, suffix, value):
    return _extend_flags_common("-DCMAKE_{}_LINKER_FLAGS".format(base),
                                suffix, value)


_LDFLAG_ARGS = [
    "exe",
    "module",
    "shared",
    "static"
]


def _make_ldflag_args():
    base_args = devpipeline.toolsupport.build_flex_args_keys(
        [["ldflags"], _LDFLAG_ARGS])
    return _make_common_args(base_args, R"ldflags\.(\w+)", R"\.(\w+)$")


_ARG_BUILDER_FUNCTIONS = [
    _make_cflag_args,
    _make_ldflag_args
]


def _make_all_options():
    # pylint: disable=global-statement
    global _ALL_CMAKE_ARGS

    if not _ALL_CMAKE_ARGS:
        cmake_args = _USABLE_ARGS.copy()
        cmake_arg_fns = _USABLE_ARG_FNS.copy()
        for arg_builder in _ARG_BUILDER_FUNCTIONS:
            new_cmake_args, new_cmake_arg_fns = arg_builder()
            cmake_args.update(new_cmake_args)
            cmake_arg_fns.update(new_cmake_arg_fns)
        _ALL_CMAKE_ARGS = (cmake_args, cmake_arg_fns)
    return _ALL_CMAKE_ARGS


_EX_ARGS = {
    "project_path": None
}

_EX_ARG_FNS = {
    "project_path": lambda v: ("project_path", v)
}


def make_cmake(current_target, common_wrapper):
    """This function initializes a CMake builder for building the project."""
    configure_args = [
        "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
    ]
    cmake_args = {}

    options, option_fns = _make_all_options()

    def _add_value(value, key):
        args_key, args_value = _EX_ARG_FNS[key](value)
        cmake_args[args_key] = args_value

    devpipeline.toolsupport.args_builder(
        "cmake", current_target, options,
        lambda v, key:
        configure_args.extend(option_fns[key](v)))
    devpipeline.toolsupport.args_builder("cmake", current_target, _EX_ARGS,
                                         _add_value)
    return common_wrapper(CMake(cmake_args, configure_args))
