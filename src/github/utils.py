import os
import sys
from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from subprocess import Popen, PIPE, STDOUT
import re
import urllib2
import tempfile
import subprocess

opener = build_opener(HTTPCookieProcessor)

def urlopen2(url, data=None, auth=True, user_agent='github-cli'):
    if auth:
        config = get_config()
        auth_dict = {'login': config['user'], 'token': config['token']}
        if data:
            data.update(auth_dict)
        else:
            data = auth_dict 
    if hasattr(data, "__iter__"):
        data = urlencode(data)
    headers = {'User-Agent' : user_agent}
    try:
        return opener.open(Request(url, data, headers))
    except urllib2.HTTPError:
        raise Exception("server problem")
    except urllib2.URLError:
        raise Exception("connection problem")
    
def get_remote_info():
    command = "git config --get remote.origin.url"
    stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, 
        stderr=PIPE).communicate()
    if stderr:
        for line in stderr.splitlines():
            print line.lower()
    elif stdout:
        line = stdout.strip()
        pattern = re.compile(r'([^:/]+)/([^/]+).git$')
        result = pattern.search(line)
        if result:
            return result.groups()
        else:
            raise Exception("invalid user and repo name")
    raise Exception("not a git repository")
    
def get_remote_info_from_option(repository):
    if "/" in repository:
        user, repo = repository.split("/")
        return user, repo
    else:
        config = get_config()
        return config['user'], repository
    
def get_config():
    required_keys = ["user", "token"]
    config = {}
    for key in required_keys:
        command = "git config --global github.%s" % key
        stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, 
            stderr=PIPE).communicate()
        if stderr:
            for line in stderr.splitlines():
                print line
            sys.exit(1)
        if stdout:
            value = stdout.strip()
            config[key] = value
        else:
            alt_help_names = {'user': 'username'}
            help_name = alt_help_names.get(key, key)
            print "error: required GitHub entry '%s' not found in global git config" % key
            print "please add it to the global git config by doing this:"
            print
            print "git config --global github.%s <your GitHub %s>" % (key, help_name)
            sys.exit(1)
    return config
    
def edit_text(text):
    editor = os.getenv('EDITOR', 'vi')
  
    f = tempfile.NamedTemporaryFile()
    f.write(text)
    f.flush()
    
    command = "%s %s" % (editor, f.name)
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print "error: editor command failed"
        sys.exit(1)
  
    changed_text = open(f.name).read()
    f.close()
    stripcomment_re = re.compile(r'^#.*$', re.MULTILINE)
    return stripcomment_re.sub('', changed_text).strip()
    
def get_prog():
    if sys.argv and sys.argv[0]:
        return os.path.split(sys.argv[0])[1]
    else:
        return '<prog>'

