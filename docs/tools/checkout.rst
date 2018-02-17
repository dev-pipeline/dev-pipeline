checkout
========

Synopsis
--------
.. code::

    checkout [-h] [targets [targets ...]]


Description
-----------
Determine the dependencies of targets and make sure the repositories are up to
date.  The tool with either perform a fresh checkout or an update
(:code:`git fetch`, :code:`hg pull`, etc.) depending on the status of the
local copy.

If no targets are specified, all targets will be checked out and updated.


Options
-------
  -h, --help            show this help message and exit


Config Options
--------------
* scm - (**Required**) The source control tool to use.  This must be one of the
  options listed in SCMs_.


SCMs
----
* git_ - Build using git.
* nothing - No checkout step.  This is useful for packages that live locally
  under the dev-pipeline project for some reason.


.. _git: ../scm/git.rst
