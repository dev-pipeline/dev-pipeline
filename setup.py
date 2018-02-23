#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name="dev-pipeline",
    version="0.1.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    license="BSD-2",
    url="https://github.com/snewell/dev-pipeline",
    project_urls={
        "Source Code": "https://github.com/snewell/dev-pipeline"
    }
)
