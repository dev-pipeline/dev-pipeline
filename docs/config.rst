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


Best Practices
--------------
A package build configuration should be as portable as the software you want
to support; try not to embed anything platform-specific (e.g., paths,
environment variables, compiler information) in your main configuration since
that could cause breakage on other systems.  If you have configuration
specific to your system, it should go in either a profile_ or overrides_.


Available Configuration Options
-------------------------------
* :code:`depends` - A comma-separated list of packages to depend on.  This is
  used by most dev-pipeline tools.

Environment variables can be customized as well.  Because different platforms
use different syntax to manipulate environments (e.g., colon-separated values
in Unix and semi-colon-separated values in Windows) these values are best set
in local files instead of a shared build.config.

* :code:`env.XXX` - Set the environment variable :code:`XXX`.
* :code:`env_append.XXX` - Append the environment variable :code:`XXX`.  If it
  isn't already set in the environment, this is equivalent to :code:`env.XXX`.


Expanded Options
----------------
Some options are dependent on factors outside the control of
:code:`build.config` (such as the absolute path of a bulid).  These values can
be used like normal.  If a :code:`build.config` sets any of these values,
results are undefined but at minimum you can expect strange behavior.

All variables provided in this manner are prefixed with :code:`dp.`.

* :code:`dp.build_config` - Full path to the build configuration used by a
  project.
* :code:`dp.build_dir` - The build directory of a specific package.  This will
  be a folder within :code:`dp.build_root`.
* :code:`dp.build_root` - The root directory for all package builds.
* :code:`dp.overrides` - A comma-separated list of overrides_ that should be
  considered for this project.
* :code:`dp.override_list` - A comma-separated list of overrides_ applied to a
  specific package.
* :code:`dp.profile_name` -  The name of the profile_ a build is configured
  for.
* :code:`dp.src_dir` - The full path to the source folder for each package.
  This will be some folder within :code:`dp.src_root`.
* :code:`dp.src_root` - The root directory where each package is checked out.


Example Configuration
---------------------
A simple :code:`build.config` looks like this.  It should be fairly
human-readable, but comments are inline to help explain.

.. code:: ini

    # Common settings for everything we're building.  These can be overriden
    # below on a case-by-case basis if the globals don't work.
    [DEFAULT]
    build = cmake
    scm = git
    cmake.prefix = /usr
    install_path = install

    # Provide information to build gtest
    [gtest]
    git.uri = https://github.com/google/googletest
    git.revision = release-1.8.0
    cmake.args =
        -DBUILD_SHARED_LIBS=ON
    # dep_args isn't used internally, but you can set arbitrary values.  In
    # this case, dep_args will be used by everything that depends on gtest.
    dep_args =
        -DGTEST_ROOT=${dp.build_dir}/${install_path}/${cmake.prefix}

    [bureaucracy]
    # Dependent packages are separated with commas.  You can depend on things
    # that haven't been declared yet (e.g., houseguest).
    depends =
        gtest,
        houseguest
    git.uri = https://github.com/snewell/bureaucracy.git
    git.revision = master
    # dep_args is being used here (from both gtest and houseguest)
    cmake.args =
        ${gtest:dep_args},
        ${houseguest:dep_args},
        -DBUREAUCRAY_BUILD_DOCS=OFF
    # bureaucracy depends on houseguest, so we'll pass along those dep_args.
    # This prevents anything that depends on bureaucracy from needing to deal
    # with all dependant packages too.
    dep_args =
        -DBureaucracy_DIR=${dp.build_dir}/${install_path}/${cmake.prefix}/share/Bureaucracy/cmake/,
        ${houseguest:dep_args}

    [houseguest]
    depends =
        gtest
    git.uri = https://github.com/snewell/houseguest.git
    git.revision = master
    cmake.args =
        ${gtest:dep_args},
        -DHOUSEGUEST_BUILD_DOCS=OFF
    dep_args =
        -DHouseguest_DIR=${dp.build_dir}/${install_path}/${cmake.prefix}/share/Houseguest/cmake


.. _overrides: overrides.rst
.. _profile: profile.rst
