import os
from setuptools import setup, find_packages

version = '0.2.4'

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
    test_suite = 'nose.collector',
)

