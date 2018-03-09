#!/usr/bin/python3

major = 0
minor = 1
patch = 0

id = (
    major << 24) | (
    minor << 16) | (
    patch << 8)
string = "{}.{}.{}".format(major, minor, patch)
