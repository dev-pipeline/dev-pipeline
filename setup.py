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

        'devpipeline.builders': [
            'nothing = devpipeline.build:_nothing_builder',
        ],

        'devpipeline.scms': [
            'nothing = devpipeline.scm:_nothing_scm',
        ],

        'devpipeline.drivers': [
            'bootstrap = devpipeline.exec.bootstrap:main',
            'build = devpipeline.exec.build:main',
            'build-order = devpipeline.exec.build_order:main',
            'checkout = devpipeline.exec.checkout:main',
            'configure = devpipeline.exec.configure:main'
        ]
    },

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
)
