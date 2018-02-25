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
    def __init__(self, executor, name, env, real):
        self.env = env
        self.executor = executor
        self.name = name
        self.real = real

    def _call_helper(self, step, fn, *fn_args):
        devpipeline.toolsupport.common_tool_helper(
            self.executor, step, self.env,
            self.name, fn, *fn_args)

    def checkout(self, repo_dir):
        self._call_helper("Checking out", self.real.checkout,
                          repo_dir)

    def update(self, repo_dir):
        self._call_helper("Updating", self.real.update,
                          repo_dir)


def scm_task(target, target_name, env, executor):
    """
    Update or a local checkout.

    Arguments
    target - The target to operate on.
    """
    scm = _make_scm(target, lambda r: SimpleTool(executor, target_name,
                                                 env, r))
    src_dir = target.get("dp.src_dir")
    scm.checkout(src_dir)
    scm.update(src_dir)
