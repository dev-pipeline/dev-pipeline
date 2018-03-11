#!/usr/bin/python3

import re

import devpipeline.toolsupport


class CMake:
    def __init__(self, ex_args, config_args):
        self.ex_args = ex_args
        self._config_args = config_args

    def configure(self, src_dir, build_dir):
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
        return [{
            "args": [
                'cmake',
                '--build',
                build_dir
            ]
        }]

    def install(self, build_dir, path=None):
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

_usable_args = {
    "args": lambda v: [x.strip() for x in v.split(",")],
    "prefix": lambda v: ["-DCMAKE_INSTALL_PREFIX={}".format(v)],
    "cc": lambda v: ["-DCMAKE_C_COMPILER={}".format(v)],
    "cxx": lambda v: ["-DCMAKE_CXX_COMPILER={}".format(v)],
    "toolchain_file": lambda v: ["-DCMAKE_TOOLCHAIN_FILE={}".format(v)],
    "build_type": lambda v: ["-DCMAKE_BUILD_TYPE={}".format(v)],
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


def _make_cflag_args():
    new_args = devpipeline.toolsupport.build_flex_args_keys([_cflag_args, _valid_flag_suffixes])
    prefix_pattern = re.compile(R"(.*)flags")
    suffix_pattern = re.compile(R"\.(\w+)$")
    ret = {}
    for arg in new_args:
        prefix_match = prefix_pattern.search(arg)
        suffix_match = suffix_pattern.search(arg)
        ret[arg] = lambda v, pm=prefix_match, sm=suffix_match: _extend_cflags(pm.group(1).upper(), sm.group(1).upper(), v)
    for arg in _cflag_args:
        prefix_match = prefix_pattern.search(arg)
        ret[arg] = lambda v, pm=prefix_match: _extend_cflags(pm.group(1).upper(), None, v)
    return ret


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
    base_args = devpipeline.toolsupport.build_flex_args_keys([ ["ldflags"], _ldflag_args])
    new_args = devpipeline.toolsupport.build_flex_args_keys([base_args, _valid_flag_suffixes])
    type_pattern = re.compile(R"ldflags\.(\w+)")
    suffix_pattern = re.compile(R"\.(\w+)$")
    ret = {}
    for arg in new_args:
        type_match = type_pattern.search(arg)
        suffix_match = suffix_pattern.search(arg)
        ret[arg] = lambda v, tm=type_match, sm=suffix_match: _extend_cflags(tm.group(1).upper(), sm.group(1).upper(), v)
    for arg in base_args:
        type_match = type_pattern.search(arg)
        ret[arg] = lambda v, tm=type_match: _extend_cflags(tm.group(1).upper(), None, v)
    return ret

_arg_builder_functions = [
    _make_cflag_args,
    _make_ldflag_args
]


def _make_all_options():
    global _all_cmake_args

    if _all_cmake_args:
        return _all_cmake_args
    else:
        _all_cmake_args = _usable_args.copy()
        for arg_builder in _arg_builder_functions:
            _all_cmake_args.update(arg_builder())
        return _all_cmake_args


_ex_args = {
    "project_path": lambda v: ("project_path", v)
}


def make_cmake(component, common_wrapper, updated_config):
    configure_args = []
    cmake_args = {}

    def add_value(v, fn):
        k, r = fn(v)
        cmake_args[k] = r

    options = _make_all_options()

    devpipeline.toolsupport.args_builder("cmake", component, options,
                                         lambda v, fn:
                                             configure_args.extend(fn(v)))
    devpipeline.toolsupport.args_builder("cmake", component, _ex_args,
                                         add_value)
    return common_wrapper(CMake(cmake_args, configure_args))
