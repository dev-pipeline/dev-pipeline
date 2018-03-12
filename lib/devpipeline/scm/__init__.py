#!/usr/bin/python3
"""This module defines a base class for all SCM handlers to inherit from."""


class Scm():

    """An interface for all scms"""

    def checkout(self, repo_dir):
        """
        Perform the initial checkout of a repository.

        Arguments
        repo_dir - The absolute path where the repository should be checked
                   out.
        """
        pass

    def update(self, repo_dir):
        """
        Update a checkout to a preferred revision.

        Arguments
        repo_dir - The absolute path where the repository is located.
        """
        pass
