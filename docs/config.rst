Configuration
=============
dev-pipeline uses an ini-style configuration.  Parsing is performed using
Python's :code:`configparser` module, so see that documentation for format
rules; extended interpolation is enabled.

Each package goes in its own section and sets the variables it needs to
function properly.  Available variables depend on the tools being invoked and
may depend on other configuration values; please check the tools you're using
for more information.

Any values set in :code:`[DEFAULT]` will be used for all packages unless
overridden.  This is useful if a value is common across all (or most) of the
packages in a configuration.


Available Configuration Options
-------------------------------
* depends - A comma-separated list of packages to depend on.  This is used by
  most dev-pipeline tools.


Expanded Options
----------------
Some options are dependent on factors outside the control of
:code:`build.config` (such as the absolute path of a bulid).  These values can
be used like normal.

All variables provided in this manner are prefixed with :code:`dp_`.

* dp_build_dir - The build directory of a specific package.  If you need this
  outside a package, store it in a local key/value pair.


Example Configuration
---------------------
.. code::

    [DEFAULT]
    # options used across projects
    build = cmake
    # cmake-specific option
    prefix = /usr

    # Declare a package
    [bureaucracy]
    # Use git for source control.  Also provide information on repository and
    # revision info
    scm = git
    uri = https://github.com/snewell/bureaucracy.git
    revision = master
    # Extra cmake-specific arguments; these are used at configuration time
    cmake_args =
            -DBUILD_DOCS=OFF,
            -DBUILD_TESTS=OFF
    install_path = _install_
    # We can set arbitrary arguments; this is used to help things that depend
    # on bureaucracy
    dep_args =
        -DBureaucracy_DIR=${dp_build_dir}/${install_path}/${prefix}/share/Bureaucracy/cmake

    # Declare another package
    [bureaucracy-test]
    # This one lives locally on my system, so no scm
    scm = nothing
    # It depends on bureaucracy
    depends = bureaucracy
    # CMake-specific arguments, including one we get from bureaucracy
    no_install =
    cmake_args =
            ${bureaucracy:dep_args}
