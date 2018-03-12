#!/usr/bin/python3
"""This module implements some helper functions and a simple SCM tool."""

import devpipeline.scm.git
import devpipeline.toolsupport

# A dictionary of all supported scm tools.  Any supported tool should provide
# an interface compatible with devpipeline.scm.Scm, but it's not required they
# inherit from that class.  They keys in should match values in the "scm"
# option in a build.config, and the value should be a function that creates an
# Scm.
_SCM_LOOKUP = {
    "git": devpipeline.scm.git.make_git,
    "nothing": lambda c, cw: cw(devpipeline.scm.Scm())
}


def _make_scm(current_target, common_wrapper):
    """
    Create an Scm for a component.

    Arguments
    component - The component being operated on.
    """
    return devpipeline.toolsupport.tool_builder(current_target["current_config"], "scm",
                                                _SCM_LOOKUP, current_target, common_wrapper)


class SimpleScm(devpipeline.toolsupport.SimpleTool):

    """This class is a simple SCM tool."""

    def __init__(self, real, current_target):
        super().__init__(current_target, real)

    def checkout(self, repo_dir):
        """This function checks out source code."""
        self._call_helper("Checking out", self.real.checkout,
                          repo_dir)

    def update(self, repo_dir):
        """This funcion updates a checkout of source code."""
        self._call_helper("Updating", self.real.update,
                          repo_dir)


def scm_task(current_target):
    """
    Update or a local checkout.

    Arguments
    target - The target to operate on.
    """
    scm = _make_scm(current_target, lambda r: SimpleScm(r, current_target))

    src_dir = current_target["current_config"].get("dp.src_dir")
    scm.checkout(src_dir)
    scm.update(src_dir)
