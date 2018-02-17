build
=====

Synopsis
--------
.. code::

    build [-h] [targets [targets ...]]


Description
-----------
This tool builds one or more targets along with their dependencies.  The
specific order of dependencies isn't guaranteed, but any package will be built
before packages that depend on it.

If no targets are specified, all targets will be built.


Options
-------
  -h, --help            show this help message and exit


Config Options
--------------
* build - (**Required**) The build tool to use.  It must be an option listed
  in Builders_.
* install_path - The path *within the build directory* to install a package.
  If unspecified, :code:`install` will be used.
* no_install - Prevent a package from being installed.


Builders
--------
* cmake_ - Build using CMake.
* nothing - No build step.  This is useful for dependencies that don't produce
  any artifacts, but are needed for some reason.


.. _cmake: ../builder/cmake.rst
