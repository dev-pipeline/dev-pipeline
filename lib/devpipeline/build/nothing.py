#!/usr/bin/python3


class Nothing:
    def configure(self, src_dir):
        pass

    def build(self):
        pass

    def install(self, path=None):
        pass


def make_nothing(component, build_dir):
    return Nothing()
