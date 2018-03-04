build
=====

Synopsis
--------
.. code::

    dev-pipeline bootstrap [-h] [--executor EXECUTOR]
                           [targets [targets ...]]


Description
-----------
This tool checks out and builds packages in a configuration with proper
dependency ordering.  The result is similar to running
:code:`dev-pipeline checkout` followed by :code:`dev-pipeline build`, but the
steps are mixed instead of performing all checkouts followed by all builds.

If no targets are specified, all targets will be used.


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
No extra options are consumed.  See the build_ and checkout_ documentation for
available options.


.. _build: build.rst
.. _checkout: checkout.rst
