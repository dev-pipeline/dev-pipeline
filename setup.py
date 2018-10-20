#!/usr/bin/python3

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="dev-pipeline",
    version="0.3.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    install_requires=[
        'dev-pipeline-core >= 0.3.0',

        # commands included by default
        'dev-pipeline-bootstrap >= 0.3.0',
        'dev-pipeline-build >= 0.3.0',
        'dev-pipeline-build-order >= 0.3.0',
        'dev-pipeline-configure >= 0.3.0',
        'dev-pipeline-scm >= 0.3.0',

        # extra builders included by default
        'dev-pipeline-cmake >= 0.3.0',

        # extra scms included by default
        'dev-pipeline-git >= 0.3.0'
    ],

    entry_points={
        "console_scripts": [
            "dev-pipeline = devpipeline.driver:main"
        ]
    },

    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ]
)
