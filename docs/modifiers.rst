Value Modifiers
===============
dev-pipeline supports the idea of modification layers for every value in a
build configuration.  The concept here is based on the functionality provided
by Yocto, where the order of modifiers is defined and consistent.

For examples, see profiles_.


Supported Modifiers
-------------------
The following modifiers are applied *in order*.  You're free to specify them
in any order you wish, but they will always be queried following this pattern
*in each modifier layer*.

- :code:`append` - Add a value to the existing value (e.g.,
  :code:`${old_value}${appended_value}`).  If the value isn't set, this is
  equivalent to :code:`override`.
- :code:`prepend` - Prepend a value to the existing value (e.g.,
  :code:`${prepended_value}${old_value}`).  If there's no current value when
  prepends are applied, they function identically to :code:`override`.
- :code:`override` - Replace an existing value.
- :code:`erase` - Remove an existing value.


Layers
------
Modifier layers are evaluated in the following order:

- Profiles_.  If a build was configured with multiple profiles, they'll be
  evaluated in the same order they were provided during configuration time.
- Overrides_.  Like proifles, projects with multiple overrides will evaluated
  them in the same order they were provided at configuration time.


.. _overrides: overrides.rst
.. _profiles: profiles.rst
