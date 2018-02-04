build
=====

Synopsis
--------
.. code::

    bootstrap [-h] [--config CONFIG] [--build-dir BUILD_DIR]
                    [targets [targets ...]]


Description
-----------
This tool checks out and builds targets and all their dependencies.  The end
result is similar to running :code:`dev-pipeline checkout` followed by
:code:`dev-pipeline build` (this tool will perform checkout, build, checkout,
build... instead of performing all checkouts followed by all builds).


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --build-dir BUILD_DIR
                        The build folder to use (default: build)


Config Options
--------------
No extra options are consumed.  See the build and checkout documentation for
available options.


.. _CMake: https://www.cmake.org
