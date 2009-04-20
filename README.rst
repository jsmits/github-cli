GitHub API - command-line interface
===================================
about
-----
for now, github-cli provides a script called gh-issues, that can be used to 
access all of GitHub's documented Issues API v2 functionality from your 
command-line

github-cli is written in python

installation
------------

create a .ghrc file in your $HOME directory with the following entries:

``login = <your github login name>``

``token = <your github token>``


you can install github-cli by:

``python setup.py install``

or

``sudo python setup.py install``

a script called gh-issues will be installed in your system's bin/ directory

usage
-----
from any directory that is part of a git working directory with an origin that
is hosted on GitHub, you can do this:

=========================================== ==========================================
command                                     info
=========================================== ==========================================
``gh-issues list [open|closed]``            show all open (default) or closed issues
``gh-issues list -v [open|closed]``         same as above, but with issue details
``gh-issues``                               same as: ``gh-issues list``
``gh-issues -v``                            same as: ``gh-issues list -v``
``gh-issues -v | less``                     pipe through less command
``gh-issues show <nr>``                     show issue <nr>
``gh-issues open``                          create a new issue
``gh-issues close <nr>``                    close issue <nr>
``gh-issues reopen <nr>``                   reopen issue <nr>
``gh-issues edit <nr>``                     edit issue <nr>
``gh-issues label add <label> <nr>``        add <label> to issue <nr>
``gh-issues label remove <label> <nr>``     remove <label> from issue <nr>
``gh-issues -h``                            show help message
=========================================== ==========================================