#!/usr/bin/python3


class Component:

    def __init__(self, name):
        self._name = name
        self._values = {}

    def add_value(self, key, value):
        self._values[key] = value


class Components:

    def __init__(self):
        self._components = {}

    def add(self, component):
        self._components[component._name] = component
