#!/usr/bin/python3

import os.path
import subprocess


class Git():
    def __init__(self, args):
        self._args = args

    def checkout(self, target_dir):
        if not os.path.isdir(target_dir):
            subprocess.check_call(['git',
                                   'clone',
                                   self._args["uri"],
                                   target_dir])
        else:
            subprocess.check_call(['git',
                                   'fetch'],
                                  cwd=target_dir)

    def update(self, target_dir):
        rev = self._args.get("revision")
        if rev:
            subprocess.check_call(['git',
                                   'checkout',
                                   rev],
                                  cwd=target_dir)


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
