=============================================
GitHub Issues API v2 - command-line interface
=============================================

**IMPORTANT**: github-cli does not function anymore since API v2 has been 
replaced by `API v3 <http://developer.github.com/v3/issues/>`_. 
A possible alternative for github-cli that addresses API v3 is Stephen 
Celis' `ghi <https://github.com/stephencelis/ghi>`_.

about
*****
`github-cli <http://github-cli.readthedocs.org/>`_ provides an 
executable called ``ghi``, that can be used to access all of `GitHub 
<https://github.com/>`_'s documented `Issues API 
<http://develop.github.com/p/issues.html>`_ (v2) functionality from your 
command-line

github-cli is written in `Python <http://www.python.org/>`_

installation
************

*on most UNIX-like systems, you'll probably need to run the following 
`install` commands as root or by using sudo*

**pip**

::

  pip install github-cli

**from source**

::

  pip install git+http://github.com/jsmits/github-cli

*or*

::

  git clone git://github.com/jsmits/github-cli.git
  cd github-cli
  python setup.py install

as a result, the ``ghi`` executable will be installed into a system ``bin`` 
directory

configuration
*************
make sure your GitHub username and API token are added to the global git config::

  git config --global github.user <your GitHub username>
  git config --global github.token <your GitHub API token>

or you can specify the environment variables GITHUB_USER and GITHUB_TOKEN

you can find the username and API token on your GitHub's account page

usage
*****
from within a working directory with a remote that is hosted on
GitHub (remote named either ``origin`` or ``github`` for git repositories or 
``default`` or ``github`` for mercurial/`hg-git <http://hg-git.github.com/>`_ repositories), you can do this (note: with
the -r option, commands can be invoked from anywhere):

::

  (github-cli)[jsmits@imac:~]$ ghi --help
  Usage: ghi command [args] [options]
  
  Examples:
  ghi list [-s open|closed|all]       show open, closed or all issues
                                      (default: open)
  ghi [-s o|c|a] -v                   same as above, but with issue details
  ghi                                 same as: ghi list
  ghi -v                              same as: ghi list -v
  ghi [-s o|c] -w                     show issues' GitHub page in web browser
                                      (default: open)
  ghi list -u <github_user>           show issues created by specified user
  
  ghi show <nr>                       show issue <nr>
  ghi show <nr> -v                    same as above, but with comments
  ghi <nr>                            same as: ghi show <nr>
  ghi <nr> -w                         show issue <nr>'s GitHub page in web
                                      browser
  ghi open (o)                        create a new issue (with $EDITOR)
  ghi open (o) -m <msg>               create a new issue with <msg> content 
                                      (optionally, use \n for new lines; first 
                                      line will be the issue title)
  ghi close (c) <nr>                  close issue <nr>
  ghi open (o) <nr>                   reopen issue <nr>
  ghi edit (e) <nr>                   edit issue <nr> (with $EDITOR)
  ghi label add (al) <label> <nr>     add <label> to issue <nr>
  ghi label remove (rl) <label> <nr>  remove <label> from issue <nr>
  ghi search (s) <term>               search for <term> (default: open)
  ghi s <term> [-s o|c] -v            same as above, but with details
  ghi s <term> -s closed              only search in closed issues
  ghi comment (m) <nr>                create a comment for issue <nr>
                                      (with $EDITOR)
  ghi comment (m) <nr> -m <msg>       create a comment for issue <nr>
                                      with <msg> content. (optionally use \n
                                      for new lines)
  ghi -r <user>/<repo>                specify a repository (can be used for
                                      all commands)
  ghi -r <repo>                       specify a repository (gets user from
                                      global git config)
  
  Description: command-line interface to GitHub's Issues API (v2)
  
  Options:
    -h, --help            show this help message and exit
    -v, --verbose         show issue details (only for show, list and search
                          commands) [default: False]
    -s STATE, --state=STATE
                          specify state (only for list and search (except `all`)
                          commands) choices are: open (o), closed (c), all (a)
                          [default: open]
    -u CREATED_BY, --user=CREATED_BY
                          issues created by <github_username> [default: all]
    -m MESSAGE, --message=MESSAGE
                          message content for opening or commenting on an issue
                          without using the editor
    -r REPO, --repo=REPO, --repository=REPO
                          specify a repository (format: `user/repo` or just
                          `repo` (latter will get the user from the global git
                          config))
    -w, --web, --webbrowser
                          show issue(s) GitHub page in web browser (only for
                          list and show commands) [default: False]
    -V, --version         show program's version number and exit
