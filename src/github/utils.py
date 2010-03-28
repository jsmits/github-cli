import os
import sys
from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from subprocess import Popen, PIPE, STDOUT
import re
import urllib2
import tempfile
import subprocess
import textwrap

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
    except urllib2.HTTPError, info:
        raise Exception("server problem (%s)" % info)
    except urllib2.URLError:
        raise Exception("connection problem")
    
def get_remote_info():
    commands = ("git config --get remote.origin.url", "hg paths default")
    for command in commands:
        stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, 
            stderr=PIPE).communicate()
        if stderr:
            for line in stderr.splitlines():
                print line.lower()
        elif stdout:
            line = stdout.strip()
            if not "github.com" in line:
                raise Exception("repository needs to be hosted on github.com")
            pattern = re.compile(r'([^:/]+)/([^/]+).git$')
            result = pattern.search(line)
            if result:
                return result.groups()
            else:
                raise Exception("invalid user and repo name")
    raise Exception("not a valid repository or not hosted on github.com")
    
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
        
class Pager(object):
    """enable paging for multiple writes

    see http://svn.python.org/view/python/branches/release25-maint/Lib/pydoc.py?view=markup
    (getpager()) for handling different circumstances or platforms
    """

    def __init__(self):
        self.proc = None
        self.file = sys.stdout # ultimate fallback
        self.cmd = ''

        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            pager_commands = ['more -EMR', 'more', 'less -MR', 'less']
            for cmd in pager_commands:
                if hasattr(os, 'system') and \
                              os.system('(%s) 2>/dev/null' % cmd) == 0:
                    self.proc = subprocess.Popen([cmd], shell=True, 
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.file = self.proc.stdin
                    self.cmd = cmd
                    break

    def write(self, text=""):
        try:
            self.file.write("%s\n" % text)
        except:
            # in case the pager cmd fails unexpectedly
            self.file = sys.stdout
            self.file.write("%s\n" % text)

    def close(self):
        if 'less' in self.cmd:
            self.write("press q to quit")
        if self.proc: 
            self.file.close()
            try:
                self.proc.wait()
            except KeyboardInterrupt:
                # TODO: should kill the self.proc here gracefully
                sys.exit(0) # close silently no matter what
                
def wrap_text(text, width=79):
    if text:
        output = []
        for part in text.splitlines():
            output.append(textwrap.fill(part, width))
        return "\n".join(output)
    return text

