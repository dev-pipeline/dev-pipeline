#!/usr/bin/python3

"""Version string for module"""

MAJOR = 0
MINOR = 2
PATCH = 0

ID = (MAJOR << 24) | (MINOR << 16) | (PATCH << 8)

STRING = "{}.{}.{}".format(MAJOR, MINOR, PATCH)
