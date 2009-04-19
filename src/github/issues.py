import os
import sys
import urllib
import simplejson

from github.utils import urlopen2
from github.utils import get_remote_info, parse_config_file

def pprint_issue(issue):
    title = "#%s %s" % (issue['number'], issue['title'])
    print title
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

def command_list(state='open'):
    url = "http://github.com/api/v2/json/issues/list/%s/%s/%s"
    user, repo = get_remote_info()
    page = urlopen2(url % (user, repo, state))
    result = simplejson.load(page)
    page.close()
    issues = result.get('issues')
    if issues:
        print
        for issue in issues:
            pprint_issue(issue)
    else:
        if result.get('error'):
            handle_error(result)
        else:
            print "no issues available"
            
def command_show(number):
    url = "http://github.com/api/v2/json/issues/show/%s/%s/%s"
    user, repo = get_remote_info()
    page = urlopen2(url % (user, repo, number))
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
            
def command_open():
    url = "http://github.com/api/v2/json/issues/open/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    title = None
    while not title:
        title = raw_input("title: ")
    body = []
    entry = raw_input("body (press control-D on a new line to finish):\n")
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
    page = urlopen2(url % (user, repo), data=post_data)
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
    
def command_close(number):
    url = "http://github.com/api/v2/json/issues/close/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    page = urlopen2(url % (user, repo, number), data=post_data)
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
    
def command_reopen(number):
    url = "http://github.com/api/v2/json/issues/reopen/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    page = urlopen2(url % (user, repo, number), data=post_data)
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
            
def command_edit(number):
    url = "http://github.com/api/v2/json/issues/edit/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    title = None
    while not title:
        title = raw_input("title: ")
    body = []
    entry = raw_input("body (press control-D on a new line to finish):\n")
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
    page = urlopen2(url % (user, repo, number), data=post_data)
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
            
def command_label(command, label, number):
    url = "http://github.com/api/v2/json/issues/label/%s/%s/%s/%s/%s"
    config = parse_config_file()
    post_data = {'login': config['login'], 'token': config['token']}
    user, repo = get_remote_info()
    label = urllib.quote(label)
    label = label.replace(".", "%2E") # this is not done by urllib.quote
    url = url % (command, user, repo, label, number)
    page = urlopen2(url, data=post_data)
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
    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if args:
        command = args[0]
        globals()['command_%s' % command](*args[1:])
    else:
        print "please provide a command"
        sys.exit(1)
        
if __name__ == '__main__':
    main()
