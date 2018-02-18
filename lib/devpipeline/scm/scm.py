#!/usr/bin/python3

import devpipeline.scm.git
import devpipeline.toolsupport

# A dictionary of all supported scm tools.  Any supported tool should provide
# an interface compatible with devpipeline.scm.Scm, but it's not required they
# inherit from that class.  They keys in should match values in the "scm"
# option in a build.config, and the value should be a function that creates an
# Scm.
_scm_lookup = {
    "git": devpipeline.scm.git.make_git,
    "nothing": lambda c: devpipeline.scm.Scm()
}


def _make_scm(component):
    """
    Create an Scm for a component.

    Arguments
    component - The component being operated on.
    """
    return devpipeline.toolsupport.tool_builder(component, "scm",
                                                _scm_lookup)


def scm_task(target):
    """
    Update or a local checkout.

    Arguments
    target - The target to operate on.
    """
    scm = _make_scm(target)
    scm.checkout(target.get("dp.src_dir"))
    scm.update(target.get("dp.src_dir"))
