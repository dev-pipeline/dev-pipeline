configure
=========

Synopsis
--------
.. code::

    configure [-h] [--config CONFIG] [--profile PROFILE]
              [--build-dir BUILD_DIR]
              [--build-dir-basename BUILD_DIR_BASENAME]


Description
-----------
Confiugure a project for dev-pipeline with an optional profile_.  More than
one profile can be specified (.e.g, :code:`--profile clang,debug`), but
earlier values will take precedence if there's a conflict.  This *also*
applies to values specified in the DEFAULTS section.

This is required before most other tools will work.


Options
-------
  -h, --help            show this help message and exit
  --config CONFIG       Build configuration file (default: build.config)
  --profile PROFILE     Build-specific profiles to use. If more than one
                        profile is required, separate their names with commas.
                        (default: None)
  --build-dir BUILD_DIR
                        Directory to store configuration. If specified,
                        --build-dir-basename will be ignored. (default: None)
  --build-dir-basename BUILD_DIR_BASENAME
                        Basename for build directory configuration (default:
                        build)


.. _profile: ../profile.rst
