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
    "nothing": lambda c, cw: cw(devpipeline.scm.Scm())
}


def _make_scm(component, common_wrapper):
    """
    Create an Scm for a component.

    Arguments
    component - The component being operated on.
    """
    return devpipeline.toolsupport.tool_builder(component, "scm",
                                                _scm_lookup, common_wrapper)


class SimpleScm(devpipeline.toolsupport.SimpleTool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checkout(self, repo_dir):
        self._call_helper("Checking out", self.real.checkout,
                          repo_dir)

    def update(self, repo_dir):
        self._call_helper("Updating", self.real.update,
                          repo_dir)


def scm_task(target, *args, **kwargs):
    """
    Update or a local checkout.

    Arguments
    target - The target to operate on.
    """
    scm = _make_scm(target, lambda r: SimpleScm(real=r, *args, **kwargs))

    src_dir = target.get("dp.src_dir")
    scm.checkout(src_dir)
    scm.update(src_dir)
