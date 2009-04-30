=============================================
GitHub Issues API v2 - command-line interface
=============================================

about
*****
`github-cli <http://github.com/jsmits/github-cli/>`_ provides a 
script called ``ghi``, that can be used to access all of `GitHub 
<http://www.github.com/>`_'s documented `Issues API 
<http://develop.github.com/p/issues.html>`_ (v2) functionality from your 
command-line

github-cli is written in `Python <http://www.python.org/>`_

installation
************

**pip**

::

  sudo pip install github-cli

**easy_install**

::

  sudo easy_install github-cli

**from source**

::

  sudo pip install -e git://github.com/jsmits/github-cli.git#egg=github-cli

*or*

::

  git clone git://github.com/jsmits/github-cli.git
  cd github-cli
  python setup.py build
  sudo python setup.py install

the ``ghi`` executable will be installed into a system ``bin`` directory

configuration
*************
make sure your GitHub username and API token are added to the global git config::

  git config --global github.user <your GitHub username>
  git config --global github.token <your GitHub API token>

you can find the username and API token on your GitHub's account page

usage
*****
inside a git working directory with an origin that is hosted on GitHub, you can 
do this (note: with the -r option, commands can be invoked from anywhere):

::

  (github-cli)[jsmits@imac:~]$ ghi --help
  Usage: ghi command [args] [options]

  Examples:
  ghi list [-s open|closed|all]          # show open, closed or all issues (default: open)
  ghi [-s o|c|a] -v                      # same as above, but with issue details
  ghi                                    # same as: ghi list
  ghi -v                                 # same as: ghi list -v
  ghi -v | less                          # pipe through less command
  ghi [-s o|c] -w                        # show issues' GitHub page in web browser (default: open)
  ghi show <nr>                          # show issue <nr>
  ghi <nr>                               # same as: ghi show <nr>
  ghi <nr> -w                            # show issue <nr>'s GitHub page in web browser
  ghi open (o)                           # create a new issue (with $EDITOR)
  ghi close (c) <nr>                     # close issue <nr>
  ghi open (o) <nr>                      # reopen issue <nr>
  ghi edit (e) <nr>                      # edit issue <nr> (with $EDITOR)
  ghi label add (al) <label> <nr>        # add <label> to issue <nr>
  ghi label remove (rl) <label> <nr>     # remove <label> from issue <nr>
  ghi search (s) <term> [-s open|closed] # search for <term> in open or closed issues (default: open)
  ghi s <term> [-s o|c] -v               # same as above, but with details
  ghi comment (m) <nr>                   # create a comment for issue <nr> (with $EDITOR)
  ghi -r <user>/<repo>                   # specify a repository (can be used for all commands)
  ghi -r <repo>                          # specify a repository (gets user from global git config)

  Description: command-line interface to GitHub's Issues API (v2)

  Options:
    -h, --help            show this help message and exit
    -v, --verbose         show issue details (only for list and search commands)
                          [default: False]
    -s STATE, --state=STATE
                          specify state (only for list and search commands)
                          [choices: (o, open), (c, closed), (a, all); default:
                          open]
    -r REPO, --repo=REPO, --repository=REPO
                          specify a repository (format: `user/repo` or just
                          `repo` (latter will get the user from the global git
                          config))
    -w, --web, --webbrowser
                          show issue(s) GitHub page in web browser (only for
                          list and show commands) [default: False]
