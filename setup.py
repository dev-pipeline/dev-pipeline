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
        'dev-pipeline-core >= 0.2.0'
    ],

    entry_points={
        "console_scripts": [
            "dev-pipeline = devpipeline.exec.driver:main"
        ],

        'devpipeline.drivers': [
            'build-order = devpipeline.exec.build_order:main',
            'configure = devpipeline.exec.configure:main'
        ]
    },

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
)
