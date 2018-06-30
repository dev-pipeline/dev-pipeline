checkout
========

Synopsis
--------
.. code::

    dev-pipeline checkout [-h] [--executor EXECUTOR]
                          [targets [targets ...]]



Description
-----------
Determine the dependencies of targets and make sure the repositories are up to
date.  The tool with either perform a fresh checkout or an update
(:code:`git fetch`, :code:`hg pull`, etc.) depending on the status of the
local copy.

If no targets are specified, all targets will be checked out and updated.


Options
-------
  -h, --help           show this help message and exit
  --executor EXECUTOR  The amount of verbosity to use. Options are "quiet"
                       (print no extra information), "verbose" (print
                       additional information), "dry-run" (print commands to
                       execute, but don't run them), and "silent" (print
                       nothing). Regardless of this option, errors are always
                       printed. (default: quiet)



Config Options
--------------
* :code:`scm` - (**Required**) The source control tool to use.  Available
  options are a union of what's built in and what's available via plugins.
* :code:`src_path` - The path where a package's source tree lives.  If
  unspecified, packages will be checked out in a folder matching their name
  under :code:`dp.src_root`.


Supported SCMs
--------------
Options here are officially supported by dev-pipeline.  Other options may be
available using third-party, non-supported plugins.

* git_ - (**Requires the git plugin**) Build using git.
* nothing - No checkout step.  This is useful for packages that live locally
  under the dev-pipeline project for some reason.


.. _git: https://github.com/dev-pipeline/dev-pipeline-git/blob/master/docs/scm-git.rst
