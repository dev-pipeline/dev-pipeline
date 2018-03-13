Build Profile
=============
A build profile is a method of providing extra information to dev-pipeline
that you don't want to add in your main configuration.  Good examples are
cross-compiler information or build flags, but you can put any valid key value
pair in your profile.

The profile configuration is stored in
:code:`${HOME_DIRECTORY}/.dev-pipeline.d/profiles.conf` but is otherwise
identical to a build.config file.

The options in a profile should *always* have a modifier_ suffix.


Example
-------
.. code:: ini

    # I want to put all my favorite flags in one place so I get them when
    # using profiles.  Since these are the flags I like, I named the profile
    # after myself.
    [newell]
    cmake.cflags.append = -pipe -Wall -Wextra -Wshadow -Wundef -pedantic
    cmake.cflags.debug.append = -ggdb3 -O0
    cmake.cflags.release.append = -O2
    # I can still reference other variables here
    cmake.cxxflags.append = ${cmake.cflags.append}
    cmake.cxxflags.debug.append = ${cmake.cflags.debug.append}
    cmake.cxxflags.release.append = ${cmake.cflags.release.append}

    # I like to have each profile do a specific thing since they can be
    # stacked.  Let's make debug/release profiles.
    [debug]
    cmake.build_type.override = Debug

    [release]
    cmake.build_type.override = Release

    # I like to build with clang sometimes, so set the required values.
    [clang]
    camke.cc.override = clang
    cmake.cxx.override = clang++

    # This profile is intended to be used with the clang profile
    [libc++]
    cmake.cxxflags.append = -stdlib=libc++

    # /usr/bin/gcc is 6.4.0 on my systme, but sometimes I want to use
    # something more modern
    [gcc-7]
    cmake.cc.override = gcc-7.3.0
    cmake.cxx.override = g++-7.3.0

    # I also keep a mingw64 compiler around, so I want that available as a
    # profile option.
    [mingw64]
    cmake.toolchain_file.override = /home/stephen/cmake_toolchains/mingw64.cmake


.. _modifier: modifiers.rst
