GitHub API - command-line interface
===================================
about
*****
for now, `github-cli <http://github.com/jsmits/github-cli/>`_ provides a 
script called ``gh-issues``, that can be used to access all of `GitHub 
<http://www.github.com/>`_'s documented `Issues API 
<http://develop.github.com/p/issues.html>`_ (v2) functionality from your 
command-line

github-cli is written in `Python <http://www.python.org/>`_

installation
************

**pip**

``pip install github-cli``

**easy_install**

``easy_install github-cli``

**from source**

``pip install -e git://github.com/jsmits/github-cli.git#egg=github-cli``

or

``git clone git://github.com/jsmits/github-cli.git``

``cd github-cli``

``python setup.py install``

the ``gh-issues`` executable will be installed to a system ``bin`` directory

configuration
*************
make sure your GitHub username and API token are added to the global git 
config:

``git config --global github.user <your GitHub username>``

``git config --global github.token <your GitHub API token>``

you can find the username and API token on your GitHub's account page

usage
*****
from any directory that is part of a git working directory with an origin that
is hosted on GitHub, you can do this:

=============================================== ================================================================
command                                         info
=============================================== ================================================================
``gh-issues list [-s open|closed|all]``         show open, closed or all issues (default: open)
``gh-issues list [-s open|closed|all] -v``      same as above, but with issue details
``gh-issues``                                   same as: ``gh-issues list``
``gh-issues -v``                                same as: ``gh-issues list -v``
``gh-issues -v | less``                         pipe through less command
``gh-issues show <nr>``                         show issue <nr>
``gh-issues open``                              create a new issue
``gh-issues close <nr>``                        close issue <nr>
``gh-issues reopen <nr>``                       reopen issue <nr>
``gh-issues edit <nr>``                         edit issue <nr>
``gh-issues label add <label> <nr>``            add <label> to issue <nr>
``gh-issues label remove <label> <nr>``         remove <label> from issue <nr>
``gh-issues search <term> [-s open|closed]``    search for <term> in open or closed issues (default: open)
``gh-issues search <term> [-s open|closed] -v`` same as above, but with details
``gh-issues comment <nr>``                      create a comment for issue <nr>
``gh-issues -r <user>/<repo>``                  specify a repository
``gh-issues -r <repo>``                         specify a repository (user comes from global git config)
``gh-issues -h``                                show help message
=============================================== ================================================================