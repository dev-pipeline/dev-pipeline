build
=====

Synopsis
--------
.. code::

    bootstrap [-h] [--config CONFIG] [--build-dir BUILD_DIR]


Description
-----------
This tool checks out and builds every package in a configuration with proper
dependency ordering.  The result is similar to running
:code:`dev-pipeline checkout` followed by :code:`dev-pipeline build`, but
against all possible targets.


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --context CONTEXT     Build-specific context to use (default: None)
  --build-dir BUILD_DIR
                        The build folder to use (default: build)


Config Options
--------------
No extra options are consumed.  See the build and checkout documentation for
available options.


.. _CMake: https://www.cmake.org
