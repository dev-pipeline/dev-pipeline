checkout
========

Synopsis
--------
.. code::

    checkout [-h] [--config CONFIG] [--build-dir BUILD_DIR]
                   [targets [targets ...]]


Description
-----------
Determine the dependencies of targets and make sure the repositories are up to
date.  The tool with either perform a fresh checkout or an update
(:code:`git fetch`, :code:`hg pull`, etc.) depending on the status of the
local copy.


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --build-dir BUILD_DIR
                        The build folder to use (default: build)


Config Options
--------------
* scm - (**Required**) The source control tool to use.  This must be one of the
  options listed in SCMs_.
* revision - The revision to use during checkouts.  If unspecified, the
  repository will be checked out in whatever state the SCM chooses. In
  practice this is required, since without it the repository state will be
  unreliable.


SCMs
----
* git_ - Build using git.
* nothing - No checkout step.  This is useful for packages that live locally
  under the dev-pipeline project for some reason.


.. _git: ../scm/git.rst
