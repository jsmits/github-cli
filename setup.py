import os
import sys
from setuptools import setup, find_packages

description = "A command-line interface to the GitHub Issues API v2."
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.rst')).read()
except:
    long_description = description

# needed for importing github.version
sys.path.insert(0, os.path.join(cur_dir, 'src'))
from github.version import get_version

setup(
    name = "github-cli",
    version = get_version('short'),
    url = 'http://packages.python.org/github-cli',
    license = 'BSD',
    description = description,
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
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Bug Tracking',
    ],
    test_suite = 'nose.collector',
)
