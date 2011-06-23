import os
import sys
import re
import urllib2
import tempfile
import subprocess
import textwrap
from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from subprocess import Popen, PIPE, STDOUT

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
    headers = {'User-Agent': user_agent}
    try:
        return opener.open(Request(url, data, headers))
    except urllib2.HTTPError, info:
        raise Exception("server problem (%s)" % info)
    except urllib2.URLError:
        raise Exception("connection problem")


def get_remote_info():
    commands = (
        "git config --get remote.origin.url",
        "git config --get remote.github.url",
        "hg paths default",
        "hg paths github")
    aliases = get_aliases()
    for command in commands:
        stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
            stderr=PIPE).communicate()
        if stdout:
            line = stdout.strip()
            if not "github.com" in line:
                # check if it's using an alias
                for alias in aliases:
                    if line.startswith(alias):
                        line = line.replace(alias, aliases[alias])
                        break
                else:
                    continue
            pattern = re.compile(r'([^:/]+)/([^/]+).git$')
            result = pattern.search(line)
            if result:
                return result.groups()
            else:
                # Whilst repos are usually configured with a postfix of ".git"
                # this is by convention only. Github happily handles requests
                # without the postfix.
                pattern = re.compile(r'([^:/]+)/([^/]+)')
                result = pattern.search(line)
                if result:
                    return result.groups()
                raise Exception("invalid user and repo name")
        elif stderr:
            for line in stderr.splitlines():
                line = line.lower()
                # a bit hackish: hg paths <path> returns 'not found!' when
                # <path> is not in .hg/hgrc; this is to avoid showing it
                if not 'not found' in line:
                    print line
    raise Exception("not a valid repository or not hosted on github.com")


def get_aliases():
    """
    Return a dict of global git aliases regarding github, or None:
        {
         "alias": "http://...",
         "alias2": "git://...it",
        }
    """
    cmd = "git config --global --get-regexp url\..*github.com.*"
    stdout, stderr = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
        stderr=PIPE).communicate()
    if stdout:
        d = {}
        for alias in stdout.strip().split('\n'):
            url, alias = alias.split()
            d[alias] = url.split('.', 1)[1].rsplit('.', 1)[0]
        return d
    return []


def get_remote_info_from_option(repository):
    if "/" in repository:
        user, repo = repository.split("/")
        return user, repo
    else:
        config = get_config()
        return config['user'], repository


def get_config():
    required_keys = {
        'user': 'GITHUB_USER',
        'token': 'GITHUB_TOKEN'
    }
    config = {}
    for key, env_key in required_keys.items():
        value = os.environ.get(env_key)
        if not value:
            command = "git config --global github.%s" % key
            stdout, stderr = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
                stderr=PIPE).communicate()
            if stderr:
                for line in stderr.splitlines():
                    print line
                sys.exit(1)
            value = stdout.strip()
        if value:
            config[key] = value
        else:
            alt_help_names = {'user': 'username'}
            help_name = alt_help_names.get(key, key)
            print "error: required GitHub entry '%s' not found in global "\
                "git config" % key
            print "please add it to the global git config by doing this:"
            print
            print "    git config --global github.%s <your GitHub %s>" % (key,
                help_name)
            print
            print "or by specifying environment variables GITHUB_USER and "\
				"GITHUB_TOKEN"
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

    see http://svn.python.org/view/python/branches/release25-maint/Lib/\
    pydoc.py?view=markup
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
                sys.proc.kill()
                sys.exit(1)



def wrap_text(text, width=79):
    if text:
        output = []
        for part in text.splitlines():
            output.append(textwrap.fill(part, width))
        return "\n".join(output)
    return text


def get_underline(text, max_width=79):
    if len(text) > max_width:
        return "-" * max_width
    else:
        return "-" * len(text)
