from setuptools import setup, find_packages

version = '0.1.9'

setup(
    name = "github-cli",
    version = version,
    url = 'http://github.com/jsmits/github-cli',
    license = 'BSD',
    description = "A command-line interface to Github's API.",
    long_description = """for now, `github-cli <http://github.com/jsmits/github-cli/>`_ 
provides a script called ``gh-i``, that can be used to access all of `GitHub 
<http://www.github.com/>`_'s documented `Issues API <http://develop.github.com/p/issues.html>`_ 
(v2) functionality from your command-line""",
    author = 'Sander Smits',
    author_email = 'jhmsmits@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'simplejson'],
    entry_points="""
    [console_scripts]
    gh-i = github.issues:main
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
)