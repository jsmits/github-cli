"""fabric commands for building sphinx docs

note 1): tested with Fabric 0.9.0

full command: $ fab deploy
"""
import os

from fabric.api import *

cur_dir = os.path.dirname(os.path.abspath(__file__))

def sphinxbuild():
    local('sphinx-build -b html %s %s/html' % \
        (os.path.join(cur_dir, 'source'), 
         os.path.join(cur_dir, 'build')))
        
def create_zip():
    # create zip for pypi, for example
    local('cd %s && zip -r github-cli *' % os.path.join(cur_dir, 'build/html'))

def clean():
    local('rm -rf %s' % os.path.join(cur_dir, 'build'))

def build():
    clean()
    sphinxbuild()
    create_zip()

    
    

    
