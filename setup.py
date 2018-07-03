#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name="dev-pipeline",
    version="0.2.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    entry_points={
        "console_scripts": [
            "dev-pipeline = devpipeline.exec.driver:main"
        ],

        'devpipeline.builders': [
            'nothing = devpipeline.build:_nothing_builder',
        ],

        'devpipeline.scms': [
            'nothing = devpipeline.scm:_nothing_scm',
        ]
    },

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
)
