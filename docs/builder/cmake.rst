cmake
=====
A builder that uses CMake.


Configuration Options
---------------------
- cmake_args - A comma-separated list of extra options to pass to cmake at
  configuration time.  These will usually be in the form of
  :code:`-DCMAKE_OPTION=Whatever`, but you can pass anything you want.
- prefix - The filesystem prefix to install packages.  This will be used as
  part of the :code:`-DCMAKE_PREFIX` argument.  It's probably only necessary if
  you're using artifacts between components since the prefix will be part of
  their installation path.
