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
    "nothing": lambda c, cw: cw(devpipeline.scm.CommonScm())
}


def _make_scm(component, common_wrapper):
    """
    Create an Scm for a component.

    Arguments
    component - The component being operated on.
    """
    return devpipeline.toolsupport.tool_builder(component, "scm",
                                                _scm_lookup, common_wrapper)


class SimpleTool(devpipeline.scm.Scm):
    def __init__(self, executor, name, real):
        self.executor = executor
        self.name = name
        self.real = real

    def checkout(self, repo_dir):
        self.executor.message("Checking out {}".format(self.name))
        args = self.real.checkout(repo_dir)
        if args:
            self.executor.execute(**args)
        else:
            self.executor.message("\t(Nothing to do)")

    def update(self, repo_dir):
        self.executor.message("Updating {}".format(self.name))
        args = self.real.update(repo_dir)
        if args:
            self.executor.execute(**args)
        else:
            self.executor.message("\t(Nothing to do)")


def scm_task(target, target_name, executor):
    """
    Update or a local checkout.

    Arguments
    target - The target to operate on.
    """
    scm = _make_scm(target, lambda r: SimpleTool(executor, target_name, r))
    src_dir = target.get("dp.src_dir")
    scm.checkout(src_dir)
    scm.update(src_dir)
