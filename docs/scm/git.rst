git
===
An scm tool that works with git.


Configuration Options
---------------------
- git.uri - (**Required**) The URI of the upstream repository to clone.
- git.revision - A reference to a tree for dev-pipeline to check out.  This
  will be passed directly to a :code:`git checkout` command, so you can be
  flexible with this option.  In practice, tags and branches are probably most
  useful.
