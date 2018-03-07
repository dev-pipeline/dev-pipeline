Build Profile
=============
A build profile is a method of providing extra information to dev-pipeline
that you don't want to add in your main configuration.  Good examples are
cross-compiler information or build flags, but you can put any valid key value
pair in your profile.

The profile configuration is stored in
:code:`${HOME_DIRECTORY}/.dev-pipeline.d/profiles.conf` but is otherwise
identical to a build.config file.


Example
-------
.. code:: ini

    # I want to put all my favorite flags in one place so I get them when
    # using profiles.  Since these are the flags I like, I named the profile
    # after myself.
    [newell]
    cmake.cflags = -pipe -Wall -Wextra -Wshadow -Wundef -pedantic
    cmake.cflags.debug = -ggdb3 -O0
    cmake.cflags.release = -O2
    # I can still reference other variables here
    cmake.cxxflags = ${cmake.cflags}
    cmake.cxxflags.debug = ${cmake.cflags.debug}
    cmake.cxxflags.release = ${cmake.cflags.release}

    # I like to have each profile do a specific thing since they can be
    # stacked.  Let's make debug/release profiles.
    [debug]
    cmake.build_type = Debug

    [release]
    cmake.build_type = Release

    # I like to build with clang sometimes, so set the required values.
    [clang]
    camke.cc = clang
    cmake.cxx = clang++

    # This profile is intended to be used with the clang profile
    [libc++]
    # If I use multiple profiles, cmake.cxxflags will be appended
    cmake.cxxflags = -stdlib=libc++

    # I also keep a mingw64 compiler around, so I want that available as a
    # profile option.
    [mingw64]
    cmake.toolchain_file = /home/stephen/cmake_toolchains/mingw64.cmake
