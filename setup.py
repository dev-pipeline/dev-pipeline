#!/usr/bin/python3

from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()

_VERSION = "0.4.0"

setup(
    name="dev-pipeline",
    version=_VERSION,
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    install_requires=[
        "dev-pipeline-core >= {}".format(_VERSION),
        # commands included by default
        "dev-pipeline-bootstrap >= {}".format(_VERSION),
        "dev-pipeline-build >= {}".format(_VERSION),
        "dev-pipeline-build-order >= {}".format(_VERSION),
        "dev-pipeline-configure >= {}".format(_VERSION),
        "dev-pipeline-scm >= {}".format(_VERSION),
        # extra builders included by default
        "dev-pipeline-cmake >= {}".format(_VERSION),
        # extra scms included by default
        "dev-pipeline-git >= {}".format(_VERSION),
    ],
    entry_points={"console_scripts": ["dev-pipeline = devpipeline.driver:main"]},
    author="Stephen Newell",
    description="Manage projects spread across multiple repositories",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
)
