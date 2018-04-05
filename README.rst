dev-pipeline
============
|codacy|
|code-climate|

A tool to help manage projects with dependencies spread across repositories.


Inspiration
-----------
I work on several projects spread across repositories; some of these leverage
sub-repositories in some form, and it's led to additional complexity trying to
stay in sync (especially when dealing with merges, release lines, hot fixes,
and all the other fun things that happen in large software projects).  The
goal here is to have a suite of scripts to help keep repositories in sync and
working well together, without the issues that sub-repositories introduce.


Installation
------------
dev-pipeline requires python3; python2 will not work.

The simplest way to install is using pip_.

.. code:: bash

    $ cd /path/to/dev-pipeline
    $ pip3 install

If you don't have pip available, you can run :code:`setup.py` directly.

.. code:: bash

    $ cd /path/to/dev-pipeline
    $ python3 setup.py install

If the install completes without errors, then you're good to go.

Depending on your project configuration you may need to install additional
tools such as cmake or git; installing those tools is beyond the scope of this
document.


Using
-----
The first thing you'll need to do is write a `build configuration`_.  Once
you're ready, configure_ a build directory.

.. code:: bash

    # configure with default settings
    $ dev-pipeline configure

If everything went well, you're ready to build.

.. code:: bash

    # enter whatever directory the configure step used
    $ cd build
    # bootstrap will both pull the package sources and build them
    $ dev-pipeline bootstrap

That's it.  Check the tool documentation for information on what's available.


Common Tools
------------
* configure_ - Prepare an environment for dev-pipeline to operate.  This is
  required before most tools will work.
* bootstrap_ - Fetch sources and build packages in dependecy order.
* build_ - Build packages in dependency order.  This tool assumes the sources
  are available.
* checkout_ - Fetch sources in dependecy order.
* build-order_ - Determine the order to build a set of packages, including any
  dependencies.


.. |codacy| image:: https://api.codacy.com/project/badge/Grade/0d9cf1d52ca846dc99de6cc621dfeb7b
    :target: https://www.codacy.com/app/snewell/dev-pipeline?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dev-pipeline/dev-pipeline&amp;utm_campaign=Badge_Grade

.. |code-climate| image:: https://api.codeclimate.com/v1/badges/9427722fafe270b6716f/maintainability
   :target: https://codeclimate.com/github/dev-pipeline/dev-pipeline/maintainability
   :alt: Maintainability

.. _build configuration: docs/config.rst
.. _bootstrap: docs/tools/bootstrap.rst
.. _build: docs/tools/build.rst
.. _build-order: docs/tools/build-order.rst
.. _checkout: docs/tools/checkout.rst
.. _configure: docs/tools/configure.rst
.. _pip: https://pypi.python.org/pypi/pip
