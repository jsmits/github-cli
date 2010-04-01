import os
import sys
from nose.tools import assert_raises

from github.issues import main

repo = 'jsmits/github-cli-public-test'
prog = 'ghi'


def test_commands():
    for cmd, exp in test_input:
        def check_command(cmd, exp):
            base = [prog, '-r', repo]
            args = cmd.split(' ')
            if not args == ['']: # need this for 'just `ghi`' command test
                base.extend(args)
            sys.argv = base
            if type(exp) == type(Exception):
                assert_raises(exp, main)
            else:
                output = main()
                assert output == exp
        check_command.description = "command: %s %s" % (prog, cmd)
        yield check_command, cmd, exp

test_input = (
    # list commands
    ('list', None), ('list -v', None), ('', None), ('-v', None),
    ('lis', "error: command 'lis' not implemented"),
    ('l', "error: command 'l' not implemented"),
    ('list -s open', None), ('list -s o', None), ('list -s closed', None),
    ('list -s c', None), ('list -s all', None), ('list -s a', None),
    ('-s a', None), ('-s a -v', None), ('list -s close', SystemExit),

    # show commands
    ('show 1', None), ('1', None), ('17288182', "error: server problem (HTTP"\
        " Error 403: Forbidden)"),

    # state modification commands
    ('close 1', None), ('open 1', None), ('c 1', None), ('close 1', None),
    ('o 1', None), ('open 1', None),

    # label commands
    ('label add testing 1', None), ('label remove testing 1', None),
    ('al testing 1', None), ('rl testing 1', None),
    ('label add testing', "error: number required\nexample: ghi label add "\
        "testing 1"),

    # help commands
    ('--help', SystemExit), ('-h', SystemExit),

    # browser commands
    ('-w', SystemExit), ('1 -w', SystemExit),

    # search commands
    ('search test', None), ('s test', None), ('search test -s open', None),
    ('search test -s o', None), ('search test -s closed', None),
    ('search test -s c', None), ('s test -s c', None), ('search', SystemExit),
)
