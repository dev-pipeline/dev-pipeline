#!/usr/bin/python3

import os.path
import subprocess

import devpipeline.common


class Git():
    def __init__(self, args):
        self._args = args

    def checkout(self, repo_dir):
        if not os.path.isdir(repo_dir):
            subprocess.check_call(['git',
                                   'clone',
                                   self._args["uri"],
                                   repo_dir])
        else:
            subprocess.check_call(['git',
                                   'fetch'],
                                  cwd=repo_dir)

    def update(self, repo_dir):
        rev = self._args.get("revision")
        if rev:
            subprocess.check_call(['git',
                                   'checkout',
                                   rev],
                                  cwd=repo_dir)


_git_args = {
    "uri": lambda v: ("uri", v),
    "revision": lambda v: ("revision", v)
}


def make_git(component):
    git_args = {}

    def add_value(v, fn):
        k, r = fn(v)
        git_args[k] = r

    devpipeline.common.args_builder("git", component, _git_args, add_value)

    if not git_args.get("uri"):
        raise Exception("Not git uri ({})".format(component._name))
    else:
        return Git(git_args)
