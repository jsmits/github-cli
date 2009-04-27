GitHub API - command-line interface
===================================
about
*****
for now, `github-cli <http://github.com/jsmits/github-cli/>`_ provides a 
script called ``gh-i``, that can be used to access all of `GitHub 
<http://www.github.com/>`_'s documented `Issues API 
<http://develop.github.com/p/issues.html>`_ (v2) functionality from your 
command-line

github-cli is written in `Python <http://www.python.org/>`_

installation
************

**pip**

``sudo pip install github-cli``

**easy_install**

``sudo easy_install github-cli``

**from source**

``sudo pip install -e git://github.com/jsmits/github-cli.git#egg=github-cli``

or

``git clone git://github.com/jsmits/github-cli.git``

``cd github-cli``

``python setup.py build``

``sudo python setup.py install``

---

the ``gh-i`` executable will be installed to a system ``bin`` directory

configuration
*************
make sure your GitHub username and API token are added to the global git 
config:

``git config --global github.user <your GitHub username>``

``git config --global github.token <your GitHub API token>``

you can find the username and API token on your GitHub's account page

usage
*****
inside a git working directory with an origin that is hosted on GitHub, you can 
do this (note: with the -r option, commands can be invoked from anywhere):

::

 (github-cli)[jsmits@imac:~]$ gh-i --help
 Usage: gh-i command [args] [options]
 
 Examples:
 gh-i list [-s open|closed|all]         # show open, closed or all issues (default: open)
 gh-i list [-s open|closed|all] -v      # same as above, but with issue details
 gh-i                                   # same as: gh-i list
 gh-i -v                                # same as: gh-i list -v
 gh-i -v | less                         # pipe through less command
 gh-i [-s open|closed] -w               # show issues' GitHub page in web browser (default: open)
 gh-i show <nr>                         # show issue <nr>
 gh-i show <nr> -w                      # show issue <nr>'s GitHub page in web browser
 gh-i open                              # create a new issue (with $EDITOR)
 gh-i close <nr>                        # close issue <nr>
 gh-i reopen <nr>                       # reopen issue <nr>
 gh-i edit <nr>                         # edit issue <nr> (with $EDITOR)
 gh-i label add <label> <nr>            # add <label> to issue <nr>
 gh-i label remove <label> <nr>         # remove <label> from issue <nr>
 gh-i search <term> [-s open|closed]    # search for <term> in open or closed issues (default: open)
 gh-i search <term> [-s open|closed] -v # same as above, but with details
 gh-i comment <nr>                      # create a comment for issue <nr> (with $EDITOR)
 gh-i -r <user>/<repo>                  # specify a repository (can be used for all commands)
 gh-i -r <repo>                         # specify a repository (gets user from global git config)
 
 Description: command-line interface to GitHub's Issues API (v2)
 
 Options:
   -h, --help            show this help message and exit
   -v, --verbose         show issue details (only for list and search commands)
                         [default: False]
   -s STATE, --state=STATE
                         specify state (only for list and search commands)
                         [default: open]
   -r REPO, --repo=REPO, --repository=REPO
                         specify a repository (format: `user/repo` or just
                         `repo` (latter will get the user from the global git
                         config))
   -w, --web, --webbrowser
                         show issue(s) GitHub page in web browser (only for
                         list and show commands) [default: False]
 