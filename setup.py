#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name="dev-pipeline",
    version="0.2.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    install_requires=[
        'dev-pipeline-core >= 0.2.0',

        # commands included by default
        'dev-pipeline-bootstrap >= 0.2.0',
        'dev-pipeline-build >= 0.2.0',
        'dev-pipeline-build-order >= 0.2.0',
        'dev-pipeline-configure >= 0.2.0',
        'dev-pipeline-scm >= 0.2.0',

        # extra builders included by default
        'dev-pipeline-cmake >= 0.2.0',

        # extra scms included by default
        'dev-pipeline-git >= 0.2.0'
    ],

    entry_points={
        "console_scripts": [
            "dev-pipeline = devpipeline.driver:main"
        ]
    },

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
)
