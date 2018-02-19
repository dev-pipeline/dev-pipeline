cmake
=====
A builder that uses CMake.


Configuration Options
---------------------
- :code:`cmake.args` - A comma-separated list of extra options to pass to
  cmake at configuration time.  These will usually be in the form of
  :code:`-DCMAKE_OPTION=Whatever`, but you can pass anything you want.
- :code:`cmake.prefix` - The filesystem prefix to install packages.  This will
  be used as part of the :code:`-DCMAKE_PREFIX` argument.  It's probably only
  necessary if you're using artifacts between components since the prefix will
  be part of their installation path.
- :code:`cmake.cc` - The C compiler to use for builds.
- :code:`cmake.cxx` - The C++ compiler to use for builds.
- :code:`cmake.toolchain_file` - A toolchain file for cross compiling.
- :code:`cmake.build_type` - The build configuration CMake should use.
  Options can be anything supported by CMake, but common values are Debug or
  Release (note the capitalization).
- :code:`cmake.cflags` - Flags used by the C compiler regardless of build
  configuration.  You can specify flags for a specific build type by setting
  :code:`cmake.cflags.debug` (or any other valid build type).
- :code:`cmake.cxxflags` - Flags used by the C++ compiler regardless of build
  configuration.  Like :code:`cmake.flags`, you can customize this based on
  build type (e.g., :code:`cmake.cxxflags.release`).
