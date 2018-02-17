Build Context
=============
A build context is a method of providing extra information to dev-pipeline
that you don't want to add in your main configuration.  Good examples are
cross-compiler information or build flags, but you can put any valid key value
pair in your context.

The context configuration is stored in :code:`${HOME_DIRECTORY}/.dev-pipeline`
but is otherwise identical to a build.config file.


Example
-------
.. code::

    # I want to put all my favorite flags in one place so I get them by
    # default when using a context
    [DEFAULT]
    cmake.cflags = -pipe -Wall -Wextra -Wshadow -Wundef -pedantic
    cmake.cflags.debug = -ggdb3 -O0
    cmake.cflags.release = -O2
    # I can still reference other variables here
    cmake.cxxflags = ${cmake.cflags}
    cmake.cxxflags.debug = ${cmake.cflags.debug}
    cmake.cxxflags.release = ${cmake.cflags.release}

    # Each section represents a context.  Because key/values in [DEFAULT]
    # are inherited, I can just set cmake.build_type.
    [debug]
    cmake.build_type = Debug

    [release]
    cmake.build_type = Release

    # I like to build with clang sometimes, so set the required values.
    [clang]
    camke.cc = clang
    cmake.cxx = clang++

    # I also keep a mingw64 compiler around, so I want that available as a
    # context option.
    [mingw64]
    cmake.toolchain_file = /home/stephen/cmake_toolchains/mingw64.cmake
