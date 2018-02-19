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

The following flags can be specialized based on build type.  For example, to
set cflags across a project use :code:`cmake.cflags`, but to set specific
flags based on Debug builds set :code:`cmake.cflags.debug`.  The flags for
each configuration will be passed to CMake if they're set, but CMake will only
use the flags based on your build type.

- :code:`cmake.cflags` - Flags used by the C compiler regardless of build
  configuration.
- :code:`cmake.cxxflags` - Flags used by the C++ compiler regardless of build
  configuration.
- :code:`cmake.ldflags.exe` - Flags used by the linker when building
  executables.
- :code:`cmake.ldflags.module` - Flags used by the linker when building
  modules.
- :code:`cmake.ldflags.shared` - Flags used by the linker when building shared
  libraries.
- :code:`cmake.ldflags.static` - Flags used by the linker when building static
  libraries.
