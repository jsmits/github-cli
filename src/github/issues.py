import os
import sys
import urllib
import simplejson
from optparse import OptionParser

from github.utils import urlopen2
from github.utils import get_remote_info, parse_config_file

def pprint_issue(issue, verbose=True):
    title = "#%s %s" % (issue['number'], issue['title'])
    print title
    if verbose:
        print "-" * len(title)
        print "%s" % issue['body']
        print "---"
        print "state: %s" % issue['state']
        print "%s votes" % issue['votes']
        print "created: %s" % issue['created_at']
        updated = issue.get('updated_at')
        if updated and not updated == issue['created_at']:
            print "updated: %s" % updated
        print
    
def handle_error(result):
    for msg in result['error']:
        print "error: %s" % msg['error']
        
def handle_unexpected_error(result):
    print "an unexpected error occurred"
    print "----------------------------"
    print "raw output from server:"
    print result

def command_list(state='open', verbose=False, **kwargs):
    url = "http://github.com/api/v2/json/issues/list/%s/%s/%s"
    user, repo = get_remote_info()
    url = url % (user, repo, state)
    try:
        page = urlopen2(url)
    except Exception, info:
        print "error: fetching issue list failed (%s)" % info
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issues = result.get('issues')
    if issues:
        for issue in issues:
            pprint_issue(issue, verbose)
    else:
        if result.get('error'):
            handle_error(result)
        else:
            print "no issues available"
            
def command_show(number, **kwargs):
    url = "http://github.com/api/v2/json/issues/show/%s/%s/%s"
    user, repo = get_remote_info()
    url = url % (user, repo, number)
    try:
        page = urlopen2(url)
    except Exception, info:
        print "error: fetching issue failed (%s)" % info
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issue = result.get('issue')
    if issue:
        print
        pprint_issue(issue)
    else:
        if result.get('error'):
            handle_error(result)
        else:
            handle_unexpected_error(result)
            
def command_open(**kwargs):
    url = "http://github.com/api/v2/json/issues/open/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    title = None
    while not title:
        title = raw_input("title: ")
    body = []
    entry = raw_input("body (control-D on a new line to save this issue):\n")
    while True:
        body.append(entry)
        try:
            entry = raw_input("")
        except EOFError:
            break
    body = '\r\n'.join(body)
    post_data.update({'title': title, 'body': body})
    user, repo = get_remote_info()
    print "saving issue, please wait..."
    try:
        page = urlopen2(url % (user, repo), data=post_data)
    except Exception, info:
        print "error: issue not saved (%s)" % info
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issue = result.get('issue')
    if issue:
        print
        pprint_issue(issue)
        print "issue #%s saved successfully" % issue['number']
    else:
        if result.get('error'):
            handle_error(result)
        else:
            handle_unexpected_error(result)
    
def command_close(number, **kwargs):
    url = "http://github.com/api/v2/json/issues/close/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    try:
        page = urlopen2(url % (user, repo, number), data=post_data)
    except Exception, info:
        print "error: closing issue %s failed (%s)" % (number, info)
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issue = result.get('issue')
    if issue:
        print
        pprint_issue(issue)
    else:
        if result.get('error'):
            handle_error(result)
        else:
            handle_unexpected_error(result)
    
def command_reopen(number, **kwargs):
    url = "http://github.com/api/v2/json/issues/reopen/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    try:
        page = urlopen2(url % (user, repo, number), data=post_data)
    except Exception, info:
        print "error: reopening issue %s failed (%s)" % (number, info)
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issue = result.get('issue')
    if issue:
        print
        pprint_issue(issue)
    else:
        if result.get('error'):
            handle_error(result)
        else:
            handle_unexpected_error(result)
            
def command_edit(number, **kwargs):
    url = "http://github.com/api/v2/json/issues/edit/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    title = None
    while not title:
        title = raw_input("title: ")
    body = []
    entry = raw_input("body (control-D on a new line to save this issue):\n")
    while True:
        body.append(entry)
        try:
            entry = raw_input("")
        except EOFError:
            break
    body = '\r\n'.join(body)
    post_data.update({'title': title, 'body': body})
    print "saving issue, please wait..."
    user, repo = get_remote_info()
    try:
        page = urlopen2(url % (user, repo, number), data=post_data)
    except Exception, info:
        print "error: editing issue %s failed (%s)" % (number, info)
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    issue = result.get('issue')
    if issue:
        print
        pprint_issue(issue)
        print "issue #%s saved successfully" % issue['number']
    else:
        if result.get('error'):
            handle_error(result)
        else:
            handle_unexpected_error(result)
            
def command_label(command, label, number, **kwargs):
    url = "http://github.com/api/v2/json/issues/label/%s/%s/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    label = urllib.quote(label)
    label = label.replace(".", "%2E") # this is not done by urllib.quote
    url = url % (command, user, repo, label, number)
    try:
        page = urlopen2(url, data=post_data)
    except Exception, info:
        if command == 'add':
            msg = "error: adding a label to issue %s failed (%s)"
        elif command == 'remove':
            msg = "error: removing a label from issue %s failed (%s)"
        else:
            msg = "error: changing a label for issue %s failed (%s)"
        print msg % (number, info)
        sys.exit(1)
    result = simplejson.load(page)
    page.close()
    labels = result.get('labels')
    if labels:
        print "labels for issue #%s:" % number
        for label in labels:
            print "- %s" % label
    else:
        if result.get('error'):
            handle_error(result)
        else:
            print "no labels found for issue #%s" % number
            
def main():
    usage = """usage: %prog command [args] [options]
    
Examples:
gh-issues list [open|closed]            # show all open (default) or closed issues
gh-issues list -v [open|closed]         # same as above, but with issue details
gh-issues                               # same as: gh-issues list
gh-issues -v                            # same as: gh-issues list -v
gh-issues -v | less                     # pipe through less command
gh-issues show <nr>                     # show issue <nr>
gh-issues open                          # create a new issue
gh-issues close <nr>                    # close issue <nr>
gh-issues reopen <nr>                   # reopen issue <nr>
gh-issues edit <nr>                     # edit issue <nr>
gh-issues label add <label> <nr>        # add <label> to issue <nr>
gh-issues label remove <label> <nr>     # remove <label> from issue <nr>"""
    description = """Description:
gh-issues provides a command-line interface to GitHub's Issues API (v2)"""
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
      default=False, help="show details (only for list commands)"\
      " [default: False]")
    class CustomValues: pass
    (options, args) = parser.parse_args(values=CustomValues)
    kwargs = dict([(k, v) for k, v in options.__dict__.items() \
        if not k.startswith("__")])
    if args:
        command = args[0]
    else:
        command = "list" # default
    globals()['command_%s' % command](*args[1:], **kwargs)
        
if __name__ == '__main__':
    main()
