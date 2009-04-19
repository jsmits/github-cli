import os
import sys
from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from subprocess import Popen, PIPE
import re

opener = build_opener(HTTPCookieProcessor)

def urlopen2(url, data=None, user_agent='github-cli'):
    """opens the url"""
    if hasattr(data, "__iter__"):
        data = urlencode(data)
    headers = {'User-Agent' : user_agent}
    return opener.open(Request(url, data, headers))
    
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
    
def parse_config_file():
    home_dir = os.path.expanduser("~")
    rc_file = ".ghrc"
    file_name = os.path.join(home_dir, rc_file)
    try:
        f = open(file_name, 'r')
        output = {}
        for line in f.readlines():
            line = line.strip()
            try:
                key, value = tuple(line.split("="))
                key = key.strip()
                value = value.strip()
                output.update({key: value})
            except:
                pass
        f.close()
        validate_parsed_rc(output)
        return output
    except IOError, info:
        print "could not open %s (%s)" % (file_name, info)
        sys.exit(1)
        
def validate_parsed_rc(data):
    required_keys = ['login', 'token']
    for key in required_keys:
        try:
            data[key]
        except KeyError:
            print "rc file should have a '%s' entry" % key
            sys.exit(1)

        
        
                    
