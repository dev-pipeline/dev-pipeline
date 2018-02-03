#!/usr/bin/python3

import devpipeline.scm.nothing
import devpipeline.scm.git

_scm_lookup = {
    "git": devpipeline.scm.git.make_git,
    "nothing": devpipeline.scm.nothing.make_nothing
}


def make_scm(component):
    scm = component._values.get("scm")
    if scm:
        scm_fn = _scm_lookup.get(scm)
        if scm_fn:
            return scm_fn(component)
        else:
            raise Exception(
                "Unknown scm '{}' for {}".format(scm, component._name))
    else:
        raise Exception("{} does not specify scm".format(component._name))


def scm_task(target):
    scm = make_scm(target)
    scm.checkout(target._name)
    scm.update(target._name)
