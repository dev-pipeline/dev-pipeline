#!/usr/bin/python3

import os.path

import devpipeline.toolsupport


class Git(devpipeline.scm.CommonScm):
    def __init__(self, args):
        self._args = args

    def checkout(self, repo_dir):
        if not os.path.isdir(repo_dir):
            return {
                "args": [
                    'git',
                    'clone',
                    self._args["uri"],
                    repo_dir
                ]
            }
        else:
            return {
                "args": [
                    'git',
                    'fetch'
                ],
                "cwd": repo_dir
            }

    def update(self, repo_dir):
        rev = self._args.get("revision")
        if rev:
            return {
                "args": [
                    'git',
                    'checkout',
                    rev
                ],
                "cwd": repo_dir
            }
        else:
            return None


_git_args = {
    "uri": lambda v: ("uri", v),
    "revision": lambda v: ("revision", v)
}


def make_git(component, common_wrapper):
    git_args = {}

    def add_value(v, fn):
        k, r = fn(v)
        git_args[k] = r

    devpipeline.toolsupport.args_builder("git", component, _git_args,
                                         add_value)

    if not git_args.get("uri"):
        raise Exception("Not git uri ({})".format(component._name))
    else:
        return common_wrapper(Git(git_args))
