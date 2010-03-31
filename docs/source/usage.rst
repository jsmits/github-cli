Usage
=====

From within a working directory with a remote that is hosted on
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
  ghi show <nr>                       show issue <nr>
  ghi show <nr> -v                    same as above, but with comments
  ghi <nr>                            same as: ghi show <nr>
  ghi <nr> -w                         show issue <nr>'s GitHub page in web 
                                      browser
  ghi open (o)                        create a new issue (with $EDITOR)
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
    -r REPO, --repo=REPO, --repository=REPO
                          specify a repository (format: `user/repo` or just
                          `repo` (latter will get the user from the global git
                          config))
    -w, --web, --webbrowser
                          show issue(s) GitHub page in web browser (only for
                          list and show commands) [default: False]
    -V, --version         show program's version number and exit
