Contributing to dev-pipeline
============================
Contributions should be submitted as pull requests via Github_.  If this isn't
an option for some reason we'll try to work with you, but the more hoops we
need to jump through to get and review your code the less likely anybody is to
integrate it.


Code Contributions
------------------
dev-pipeline is primarily written in Python3.  Code should be formatted
according to PEP8_, preferably with an automatic tool like autopep8_; when in
conflict, the tool *always* wins.

As a general guideline, algorithm-based implementations are appreciated.


Documentation Contributions
---------------------------
Documentation, including files like README, is written in reStructuredText_.
Please perform at least a cursory check (:code:`rst2html` or the moral
equivalent on your system) before submitting your pull request.  Documentation
should be written in American English.

Remember that while rst files are used to generate output, developers (both
those contributing to and using dev-pipeline) have to deal with the raw text.
Keep lines limited to 80 characters and consider how your change will look
when diffed.


.. _autopep8: https://pypi.python.org/pypi/autopep8
.. _Github: https://github.com/snewell/dev-pipeline
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _readme: README.rst
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
