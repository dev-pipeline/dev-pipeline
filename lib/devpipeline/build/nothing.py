#!/usr/bin/python3


class Nothing:
    def configure(self, src_dir, build_dir):
        pass

    def build(self, build_dir):
        pass

    def install(self, build_dir, path=None):
        pass


def make_nothing(component):
    return Nothing()
