"""
Tests covering version number pretty-print functionality.

Borrowed from `fabric`.
"""

from nose.tools import eq_

import github.version


def test_get_version():
    get_version = github.version.get_version
    for tup, short, normal, verbose in [
        ((0, 2, 0, 'final', 0), '0.2.0', '0.2', '0.2 final'),
        ((0, 2, 7, 'final', 0), '0.2.7', '0.2.7', '0.2.7 final'),
        ((0, 2, 0, 'alpha', 1), '0.2a1', '0.2 alpha 1', '0.2 alpha 1'),
        ((0, 2, 7, 'beta', 1), '0.2.7b1', '0.2.7 beta 1', '0.2.7 beta 1'),
        ((0, 2, 0, 'release candidate', 1),
            '0.2rc1', '0.2 release candidate 1', '0.2 release candidate 1'),
        ((1, 0, 0, 'alpha', 0), '1.0a', '1.0 pre-alpha', '1.0 pre-alpha'),
    ]:
        github.version.VERSION = tup
        yield eq_, get_version('short'), short
        yield eq_, get_version('normal'), normal
        yield eq_, get_version('verbose'), verbose
