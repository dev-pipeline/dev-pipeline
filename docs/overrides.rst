Package Overrides
=================
Package overrides are a method of providing local alterations to a package
without modifying a build.config.  They're similar in philosophy and theory to
profiles_, but overrides allow alterations at a package level.

A simple use case is changing :code:`PATH` for one package that requires a
newer version of CMake than you'd have in the regular path; that package can
use the upated tool while other packages can continue to use the default
system installation.


Format
------
Override files are located in
:code:`${HOME_DIRECTORY}/.dev-pipeline.d/overrides.d/<override-name>/<package-name>.conf`.
Files are the same section and key/value pairs as other dev-pipeline files.

Any valid key/values can be used in sections.


Sections
--------
The following sections are supported:

* :code:`append` - Add a value to a package config.  If the package doesn't
  have an option for the key, this functions identically to set.
* :code:`delete` - Remove a value.  This *will not* remove values provided by
  the DEFAULT section.
* :code:`set` - Set a value.


Example
-------
.. code:: bash

    $ cat ~/.dev-pipeline.d/overrides.d/test/gtest.conf
    [append]
    cmake.cxxflags = -Wno-error


.. _profiles: profile.rst
