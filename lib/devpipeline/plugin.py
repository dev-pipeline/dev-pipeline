#!/usr/bin/python3

import importlib
import pkgutil

import devpipeline_plugins


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def find_plugins(ns_pkg):
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(ns_pkg)
    }


_PLUGINS = None


def query_plugins(query_fn, found_fn):
    global _PLUGINS

    if not _PLUGINS:
        _PLUGINS = find_plugins(devpipeline_plugins)

    for name, module in _PLUGINS.items():
        try:
            element = getattr(module, query_fn)
            if element:
                found_fn(element())
        except AttributeError:
            pass
