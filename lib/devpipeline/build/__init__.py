#!/usr/bin/python3
"""This module defines a base class for builds to inherit from."""


class Builder:

    """A class capable of performing the build steps for a single target."""

    def configure(self, src_dir, build_dir):
        """
        Configure the build directory of a packge.

        This function prepares a build directory for later steps.  It should
        perform a step along the lines of autoconf's configure.

        Arguments
        src_dir - The absolute path to a package's source directory.
        build_dir - The absolute path to a package's build directory.  This is
                    the filesystem location where the Builder should store any
                    required files.
        """
        pass

    def build(self, build_dir):
        """
        Build a package.

        Arguments
        build_dir - The absolute path to a package's build directory.
        """
        pass

    def install(self, build_dir, path=None):
        """
        Install a package.

        Arguments
        build_dir - The absolute path to a package's build directory.
        path - The folder to install package artifacts.
        """
        pass
