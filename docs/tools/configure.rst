configure
=========

Synopsis
--------
.. code::

    dev-pipeline configure [-h] [--config CONFIG] [--profile PROFILE]
                           [--override OVERRIDE] [--build-dir BUILD_DIR]
                           [--build-dir-basename BUILD_DIR_BASENAME]


Description
-----------
Confiugure a project for dev-pipeline with an optional profile_.  More than
one profile can be specified (.e.g, :code:`--profile clang,debug`), but
if multiple profiles set the same option, their values will be appended.  This
also applies to things set in DEFAULTS, so use multiple profiles with caution.

This is required before most other tools will work.


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --profile PROFILE     Build-specific profiles to use. If more than one
                        profile is required, separate their names with commas.
                        (default: None
  --override OVERRIDE   Collection of override options to use. If you require
                        multiple types of overrides, separate the names with
                        commas. (default: None)
  --build-dir BUILD_DIR
                        Directory to store configuration. If specified,
                        --build-dir-basename will be ignored. (default: None)
  --build-dir-basename BUILD_DIR_BASENAME
                        Basename for build directory configuration (default:
                        build)


.. _profile: ../profile.rst
