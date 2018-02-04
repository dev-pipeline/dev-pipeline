#!/usr/bin/python3


class Nothing():
    def checkout(self, repo_dir):
        pass

    def update(self, repo_dir):
        pass


def make_nothing(component):
    return Nothing()
