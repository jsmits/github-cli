import os
from setuptools import setup, find_packages
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin, walk

version = '0.2.3'

class TestRunner(Command):
    """run tests with setup.py
    
    usage: python setup.py test
    """
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = [ ]
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]])
                )

        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 1)
        t.run(tests)
        
cur_dir = os.path.dirname(__file__)
readme = open(os.path.join(cur_dir, 'README.rst')).read()
long_description = readme

setup(
    name = "github-cli",
    version = version,
    url = 'http://github.com/jsmits/github-cli',
    license = 'BSD',
    description = "A command-line interface to the GitHub Issues API v2.",
    long_description = long_description,
    author = 'Sander Smits',
    author_email = 'jhmsmits@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'simplejson'],
    entry_points="""
    [console_scripts]
    ghi = github.issues:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Bug Tracking',
    ],
    cmdclass = {'test': TestRunner},
)

