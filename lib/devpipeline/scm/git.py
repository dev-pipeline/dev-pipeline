#!/usr/bin/python3

import os.path
import subprocess


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


def make_git(component):
    git_args = {}
    val = component._values.get("uri")
    if not val:
        raise Exception("Not git uri ({})".format(component._name))
    else:
        git_args["uri"] = val
    val = component._values.get("revision")
    if val:
        git_args["revision"] = val

    return Git(git_args)
