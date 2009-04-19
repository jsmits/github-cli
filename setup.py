from setuptools import setup, find_packages

version = '0.1'

setup(
    name = "github-cli",
    version = version,
    url = 'http://github.com/jsmits/github-cli',
    license = 'BSD',
    description = "A command-line interface to Github's API.",
    author = 'Sander Smits',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'simplejson'],
    entry_points="""
    [console_scripts]
    gh-issues = github.issues:main
    """
)