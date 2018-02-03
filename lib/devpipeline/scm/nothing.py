#!/usr/bin/python3


class Nothing():
    def checkout(self, target_dir):
        pass

    def update(self, target_dir):
        pass


def make_nothing(component):
    return Nothing()
