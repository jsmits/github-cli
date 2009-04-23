import os
import sys
from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from subprocess import Popen, PIPE
import re
import urllib2

opener = build_opener(HTTPCookieProcessor)

def urlopen2(url, data=None, auth=False, user_agent='github-cli'):
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
    
def get_remote_info(name='origin'):
    command = "git remote -v"
    stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, 
        stderr=PIPE).communicate()
    if stderr:
        for line in stderr.splitlines():
            print line.lower()
    if stdout:
        for line in stdout.splitlines():
            if line.startswith(name):
                pattern = re.compile(r'^git@github\.com:(.*?)\/(.*?)\.git$')
                result = pattern.search(line.split()[1])
                if result:
                    return result.groups()
                else:
                    pattern = re.compile(r'^git:\/\/github\.com\/(.*?)\/(.*?)\.git$')
                    result = pattern.search(line.split()[1])
                    if result:
                        return result.groups()
                    else:
                        print "'%s' not found on github" % name
    print "aborting script"
    sys.exit(1)
    
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
        

        
        
                    
