build
=====

Synopsis
--------
.. code::

    build [-h] [--config CONFIG] [--build-dir BUILD_DIR]
                [targets [targets ...]]


Description
-----------
This tool builds one or more targets along with their dependencies.  The
specific order of dependencies isn't guaranteed, but any package will be built
before packages that depend on it.


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --context CONTEXT     Build-specific context to use (default: None)
  --build-dir BUILD_DIR
                        The build folder to use (default: build)


Config Options
--------------
* build - (**Required**) The build tool to use.  It must be an option listed
  in Builders_.


Builders
--------
* cmake_ - Build using CMake.
* nothing - No build step.  This is useful for dependencies that don't produce
  any artifacts, but are needed for some reason.


.. _cmake: ../builder/cmake.rst
