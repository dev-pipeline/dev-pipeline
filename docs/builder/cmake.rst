cmake
=====
A builder that uses CMake.


Configuration Options
---------------------
- cmake.args - A comma-separated list of extra options to pass to cmake at
  configuration time.  These will usually be in the form of
  :code:`-DCMAKE_OPTION=Whatever`, but you can pass anything you want.
- cmake.prefix - The filesystem prefix to install packages.  This will be used
  as part of the :code:`-DCMAKE_PREFIX` argument.  It's probably only necessary
  if you're using artifacts between components since the prefix will be part of
  their installation path.
- cmake.cc - The C compiler to use for builds.
- cmake.cxx - The C++ compiler to use for builds.
- cmake.toolchain_file - A toolchain file for cross compiling.
- cmake.build_type - The build configuration CMake should use.  Options can be
  anything supported by CMake, but common values are Debug or Release (not the
  capitalization).
- cmake.cflags - Flags used by the C compiler regardless of build
  configuration.
- cmake.cxxflags - Flags used by the C++ compiler regardless of build
  configuration.
- cmake.cflags.debug - Flags used by the C compiler when the build type is
  Debug.  This will be used in addition to anything set in
  :code:`cmake.cflags`.
- cmake.cxxflags.debug - Flags used by the C++ compiler when the build type is
  Debug.  This will be used in addition to anything set in
  :code:`cmake.cxxflags`.
- cmake.cflags.release - Flags used by the C compiler when the build type is
  Release.  This will be used in addition to anything set in
  :code:`cmake.cflags`.
- cmake.cxxflags.release - Flags used by the C++ compiler when the build type
  is Release.  This will be used in addition to anything set in
  :code:`cmake.cxxflags`.
