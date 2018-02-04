#!/usr/bin/python3

import devpipeline.common
import devpipeline.scm.nothing
import devpipeline.scm.git

_scm_lookup = {
    "git": devpipeline.scm.git.make_git,
    "nothing": devpipeline.scm.nothing.make_nothing
}


def make_scm(component):
    return devpipeline.common.tool_builder(component, "scm",
                                           _scm_lookup)


def scm_task(target):
    scm = make_scm(target)
    scm.checkout(target._values["dp_src_dir"])
    scm.update(target._values["dp_src_dir"])
