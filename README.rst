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


Using
-----
dev-pipeline follows the libexec model, with a single front-end
(:code:`dev-pipeline`) that prepares the environment before invoking the
desired tool.


Installation
------------
dev-pipeline is installed using :code:`install.sh`.  Typical Unix system utils
are assumed to be installed in their usual locations, but additional tools may
be required based on the configuration of your projects.  As a general rule,
programs like :code:`git` and :code:`cmake` are expected to be in :code:`PATH`.


.. |codacy| image::
    https://api.codacy.com/project/badge/Grade/f7052d1a0fba4dde89e0e358f358b952
    :target: https://www.codacy.com/app/snewell/dev-pipeline?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=snewell/dev-pipeline&amp;utm_campaign=Badge_Grade

.. |code-climate| image::
    https://api.codeclimate.com/v1/badges/aa74c89202fefddff664/maintainability
   :target: https://codeclimate.com/github/snewell/dev-pipeline/maintainability
