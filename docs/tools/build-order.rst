build-order
===========

Synopsis
--------
.. code::

    build-order [-h] [targets [targets ...]]


Description
-----------
Display a valid order to build a set of targets along with their dependencies.
The same order is *not* guaranteed between every run, but the order will
satisfy pacakge dependencies.


Options
-------
  -h, --help       show this help message and exit
  --method METHOD  The method used to display build order. Valid options are
                   list (an order to resolve specified targets) and dot (a dot
                   graph). (default: list)


Config Options
--------------
No extra configuration options.
