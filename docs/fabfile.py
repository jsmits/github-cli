"""fabric commands for creating sphinx docs and deploying it to gh-pages

note 1): tested with Fabric 0.9a2
note 2): before usage: if needed, adapt TARGET_PATH for your own situation 

full command: $ fab deploy
"""
from __future__ import with_statement

import os
import shutil

from fabric.api import *
from fabric.context_managers import warnings_only
from fabric.state import env

CWD = os.path.dirname(os.path.abspath(__file__))
TARGET_PATH = os.path.join(CWD, "../..", "github-cli-gh-pages")

def build():
    local('sphinx-build -b html -d %s/doctrees %s %s/html' % \
        (os.path.join(CWD, 'build'),
         os.path.join(CWD, 'source'), 
         os.path.join(CWD, 'build')))
         
def copy():
    local('cp -r %s/html/* %s' % (os.path.join(CWD, 'build'), 
        TARGET_PATH))
        
def adapt():
    # first rename '_sources' and '_static' folders to 'sources' and 'static'
    to_rename_dirs = ['_sources', '_static']
    for trd in to_rename_dirs:
        dp = os.path.join(TARGET_PATH, trd)
        if os.path.exists(dp) and os.path.isdir(dp):
            target_dir = os.path.join(TARGET_PATH, trd[1:]) # removes the _
            if os.path.exists(target_dir) and os.path.isdir(target_dir):
                shutil.rmtree(target_dir)
            shutil.move(dp, target_dir) # rename
            print "renamed dir: %s to %s" % (trd, trd[1:])
            
    incl_extensions = ['html', 'js']
    for dirpath, dirnames, filenames in os.walk(TARGET_PATH):
        if '.git' in dirpath:
            continue
        for name in filenames:
            fn = os.path.join(dirpath, name)
            if os.path.splitext(fn)[1][1:] in incl_extensions:
                f = open(fn, 'r')
                text = f.read()
                f.close()
                ctext = text.replace('_sources', 'sources').replace(
                    '_static', 'static')
                if not ctext == text:
                    out = open(fn, 'w')
                    out.write(ctext)
                    out.close()
                    print "rewritten file: %s" % fn
                    
def upload():
    local('cd %s && git add . && git commit -a -m "updated" && '\
        'git push origin gh-pages' % TARGET_PATH)

def clean_build():
    local('rm -rf %s' % os.path.join(CWD, 'build'))
    
def clean_target():
    """remove files in target repo"""
    for name in os.listdir(TARGET_PATH):
        if not name.startswith('.git'):
            full_name = os.path.join(TARGET_PATH, name)
            if os.path.isdir(full_name):
                shutil.rmtree(full_name)
                print "removed dir: %s" % full_name
            elif os.path.isfile(full_name):
                os.remove(full_name)
                print "removed file: %s" % full_name

def deploy():
    clean_build()
    build()
    clean_target()
    copy()
    adapt()
    with warnings_only():
        upload()
    clean_build()
    
    

    
