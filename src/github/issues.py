import os
import sys
import urllib
import simplejson
from optparse import OptionParser

from github.utils import urlopen2, get_remote_info, create_edit_issue, \
    create_comment, get_remote_info_from_option

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
        
def validate_number(number, example):
    msg = "error: number required\nexample: %s" % example
    if not number:
        print msg
        sys.exit(1)
    else:
        try:
            int(number)
        except:
            print msg
            sys.exit(1)

def get_key(data, key):
    try:
        return data[key]
    except KeyError:
        raise Exception("unexpected failure")

class Commands(object):
    
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.url_template = "http://github.com/api/v2/json/issues/%s/%s/%s"
        
    def search(self, search_term=None, state='open', verbose=False, **kwargs):
        if not search_term:
            example = "gh-issues search experimental"
            msg = "error: search term required\nexample: %s" % example
            print msg
            sys.exit(1)
        search_term_quoted = urllib.quote_plus(search_term)
        search_term_quoted = search_term_quoted.replace(".", "%2E")
        result = self.__submit('search', search_term, state)
        issues = get_key(result, 'issues')
        print "searching for '%s' returned %s issues" % (search_term, len(issues))
        for issue in issues:
            pprint_issue(issue, verbose)
        
    def list(self, state='open', verbose=False, **kwargs):
        result = self.__submit('list', state)
        issues = get_key(result, 'issues')
        if issues:
            for issue in issues:
                pprint_issue(issue, verbose)
        else:
            print "no issues available"
        
    def show(self, number=None, **kwargs):
        validate_number(number, example="gh-issues show 1")
        issue = self.__get_issue(number)
        print
        pprint_issue(issue)
        
    def open(self, **kwargs):
        post_data = create_edit_issue()
        result = self.__submit('open', data=post_data)
        issue = get_key(result, 'issue')
        print
        pprint_issue(issue)
        
    def close(self, number=None, **kwargs):
        validate_number(number, example="gh-issues close 1")
        result = self.__submit('close', number)
        issue = get_key(result, 'issue')
        print
        pprint_issue(issue)
        
    def reopen(self, number=None, **kwargs):
        validate_number(number, example="gh-issues reopen 1")
        result = self.__submit('reopen', number)
        issue = get_key(result, 'issue')
        print
        pprint_issue(issue)
        
    def edit(self, number=None, **kwargs):
        validate_number(number, example="gh-issues edit 1")
        gh_issue = self.__get_issue(number)
        output = {'title': gh_issue['title'], 'body': gh_issue['body']}
        post_data = create_edit_issue(gh_issue)
        if post_data['title'] == output['title'] and \
                post_data['body'].splitlines() == output['body'].splitlines():
            print "no changes found"
            sys.exit(1)
        result = self.__submit('edit', number, data=post_data)
        issue = get_key(result, 'issue')
        print
        pprint_issue(issue)
        
    def label(self, command, label, number=None, **kwargs):
        validate_number(number, example="gh-issues label %s %s 1" % (command,
            label))
        if command not in ['add', 'remove']:
            msg = "label command should use either 'add' or 'remove'\n"\
                "example: gh-issues label add %s %s" % (label, number)
            raise Exception(msg)
        label = urllib.quote(label)
        label = label.replace(".", "%2E") # this is not done by urllib.quote
        result = self.__submit('label/%s' % command, label, number)
        labels = get_key(result, 'labels')
        if labels:
            print "labels for issue #%s:" % number
            for label in labels:
                print "- %s" % label
        else:
            print "no labels found for issue #%s" % number
        
    def comment(self, number=None, **kwargs):
        validate_number(number, example="gh-issues comment 1")
        gh_issue = self.__get_issue(number)
        comment = create_comment(gh_issue)
        post_data = {'comment': comment}
        result = self.__submit('comment', number, data=post_data)
        returned_comment = get_key(result, 'comment')
        if returned_comment:
            print "comment for issue #%s submitted successfully" % number
        
    def __get_issue(self, number):
        result = self.__submit('show', number)
        return get_key(result, 'issue')
        
    def __submit(self, action, *args, **kwargs):
        base_url = self.url_template % (action, self.user, self.repo)
        args_list = list(args)
        args_list.insert(0, base_url)
        url = "/".join(args_list)
        page = urlopen2(url, **kwargs)
        result = simplejson.load(page)
        page.close()
        if result.get('error'):
            handle_error(result) # should raise an Exception
            sys.exit(1)
        else:
            return result
        
def main():
    usage = """usage: %prog command [args] [options]

Examples:
%prog list [-s open|closed]             # show all open (default) or closed issues
%prog list [-s open|closed] -v          # same as above, but with issue details
%prog                                   # same as: %prog list
%prog -v                                # same as: %prog list -v
%prog -v | less                         # pipe through less command
%prog show <nr>                         # show issue <nr>
%prog open                              # create a new issue
%prog close <nr>                        # close issue <nr>
%prog reopen <nr>                       # reopen issue <nr>
%prog edit <nr>                         # edit issue <nr>
%prog label add <label> <nr>            # add <label> to issue <nr>
%prog label remove <label> <nr>         # remove <label> from issue <nr>
%prog search <term> [-s open|closed]    # search for all open (default) or closed issues containing <term>
%prog search <term> [-s open|closed] -v # same as above, but with details
%prog comment <nr>                      # create a comment for issue <nr>
%prog -r <user>/<repo>                  # specify a repository
%prog -r <repo>                         # specify a repository (gets user from global git config)"""
    
    description = """Description:
command-line interface to GitHub's Issues API (v2)"""
    
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
      default=False, help="show issue details (only for list and search "\
        "commands) [default: False]")
    parser.add_option("-s", "--state", action="store", dest="state", 
        type='choice', choices=['open', 'closed'], default='open', 
        help="specify state (only for list and search commands)"\
        " [default: open]")
    parser.add_option("-r", "--repo", "--repository", action="store", 
        dest="repo", help="specify a repository (format: "\
            "`user/repo` or just `repo` (latter will get the user from the "\
            "global git config))")
    
    class CustomValues: 
        pass
    (options, args) = parser.parse_args(values=CustomValues)
    
    kwargs = dict([(k, v) for k, v in options.__dict__.items() \
        if not k.startswith("__")])
    if args:
        cmd = args[0]
    else:
        cmd = "list" # default
    if cmd == 'search':
        search_term = " ".join(args[1:])
        args = (args[0], search_term)
    
    try:
        repository = kwargs.get('repo')
        if repository:
            user, repo = get_remote_info_from_option(repository)
        else:    
            user, repo = get_remote_info()
        commands = Commands(user, repo)
        getattr(commands, cmd)(*args[1:], **kwargs)
    except AttributeError:
        print "error: command '%s' not implemented" % cmd
    except Exception, info:
        print "error: %s" % info

if __name__ == '__main__':
    main()