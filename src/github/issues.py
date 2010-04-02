import os
import sys
import urllib
import webbrowser as browser
from optparse import OptionParser

try:
    import simplejson
except ImportError:
    print "error: simplejson required"
    sys.exit(1)

from github.utils import urlopen2, get_remote_info, edit_text, \
    get_remote_info_from_option, get_prog, Pager, wrap_text, get_underline
from github.version import get_version


def format_issue(issue, verbose=True):
    output = []
    if verbose:
        indent = ""
    else:
        indent = " " * (5 - len(str(issue['number'])))
    title = "%s%s. %s" % (indent, issue['number'], issue['title'])
    if not verbose:
        output.append(title[:80])
    if verbose:
        title = wrap_text(title)
        output.append(title)
        underline = get_underline(title)
        output.append(underline)
        if issue['body']:
            body = wrap_text(issue['body'])
            output.append(body)
        output.append("    state: %s" % issue['state'])
        output.append("     user: %s" % issue['user'])
        output.append("    votes: %s" % issue['votes'])
        output.append("  created: %s" % issue['created_at'])
        updated = issue.get('updated_at')
        if updated and not updated == issue['created_at']:
            output.append("  updated: %s" % updated)
        output.append(" comments: %s" % issue.get('comments', 0))
        output.append(" ")
    return output


def format_comment(comment, nr, total):
    timestamp = comment.get("updated_at", comment["created_at"])
    title = "comment %s of %s by %s (%s)" % (nr, total, comment["user"],
        timestamp)
    output = [title]
    underline = get_underline(title)
    output.append(underline)
    body = wrap_text(comment['body'])
    output.append(body)
    return output


def pprint_issue(issue, verbose=True):
    lines = format_issue(issue, verbose)
    lines.insert(0, " ") # insert empty first line
    print "\n".join(lines)


def handle_error(result):
    output = []
    for msg in result['error']:
        if msg == result['error'][0]:
            output.append(msg['error'])
        else:
            output.append("error: %s" % msg['error'])
    error_msg = "\n".join(output)
    raise Exception(error_msg)


def validate_number(number, example):
    msg = "number required\nexample: %s" % example
    if not number:
        raise Exception(msg)
    else:
        try:
            int(number)
        except:
            raise Exception(msg)


def get_key(data, key):
    try:
        return data[key]
    except KeyError:
        raise Exception("unexpected failure")


def create_edit_issue(issue=None):
    main_text = """# Please explain the issue.
# The first line will be used as the title.
# Lines starting with `#` will be ignored."""
    if issue:
        issue['main'] = main_text
        template = """%(title)s
%(body)s
%(main)s
#
#    number:  %(number)s
#      user:  %(user)s
#     votes:  %(votes)s
#     state:  %(state)s
#   created:  %(created_at)s""" % issue
    else:
        template = "\n%s" % main_text
    text = edit_text(template)
    if not text:
        raise Exception("can not submit an empty issue")
    lines = text.splitlines()
    title = lines[0]
    body = "\n".join(lines[1:]).strip()
    return {'title': title, 'body': body}


def create_comment(issue):
    inp = """
# Please enter a comment.
# Lines starting with `#` will be ignored.
#
#    number:  %(number)s
#      user:  %(user)s
#     votes:  %(votes)s
#     state:  %(state)s
#   created:  %(created_at)s""" % issue
    out = edit_text(inp)
    if not out:
        raise Exception("can not submit an empty comment")
    lines = out.splitlines()
    comment = "\n".join(lines).strip()
    return comment


class Commands(object):

    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.url_template = "http://github.com/api/v2/json/issues/%s/%s/%s"

    def search(self, search_term=None, state='open', verbose=False, **kwargs):
        if not search_term:
            example = "%s search experimental" % get_prog()
            msg = "error: search term required\nexample: %s" % example
            print msg
            sys.exit(1)
        search_term_quoted = urllib.quote_plus(search_term)
        search_term_quoted = search_term_quoted.replace(".", "%2E")
        result = self.__submit('search', search_term, state)
        issues = get_key(result, 'issues')
        header = "# searching for '%s' returned %s issues" % (search_term,
            len(issues))
        printer = Pager()
        printer.write(header)
        for issue in issues:
            lines = format_issue(issue, verbose)
            printer.write("\n".join(lines))
        printer.close()

    def list(self, state='open', verbose=False, webbrowser=False, **kwargs):
        if webbrowser:
            issues_url_template = "http://github.com/%s/%s/issues/%s"
            if state == "closed":
                issues_url = issues_url_template % (self.user, self.repo,
                    state)
            else:
                issues_url = issues_url_template % (self.user, self.repo, "")
            try:
                browser.open(issues_url)
            except:
                print "error: opening page in web browser failed"
            else:
                sys.exit(0)

        if state == 'all':
            states = ['open', 'closed']
        else:
            states = [state]
        printer = Pager()
        for st in states:
            header = "# %s issues on %s/%s" % (st, self.user, self.repo)
            printer.write(header)
            result = self.__submit('list', st)
            issues = get_key(result, 'issues')
            if issues:
                for issue in issues:
                    lines = format_issue(issue, verbose)
                    printer.write("\n".join(lines))
            else:
                printer.write("no %s issues available" % st)
            if not st == states[-1]:
                printer.write() # new line between states
        printer.close()

    def show(self, number=None, verbose=False, webbrowser=False, **kwargs):
        validate_number(number, example="%s show 1" % get_prog())
        if webbrowser:
            issue_url_template = "http://github.com/%s/%s/issues/%s/find"
            issue_url = issue_url_template % (self.user, self.repo, number)
            try:
                browser.open(issue_url)
            except:
                print "error: opening page in web browser failed"
            else:
                sys.exit(0)

        issue = self.__get_issue(number)
        if not verbose:
            pprint_issue(issue)
        else:
            printer = Pager()
            lines = format_issue(issue, verbose=True)
            lines.insert(0, " ")
            printer.write("\n".join(lines))
            if issue.get("comments", 0) > 0:
                comments = self.__submit('comments', number)
                comments = get_key(comments, 'comments')
                lines = [] # reset
                total = len(comments)
                for i in range(total):
                    comment = comments[i]
                    lines.extend(format_comment(comment, i+1, total))
                    lines.append(" ")
                printer.write("\n".join(lines))
            printer.close()

    def open(self, **kwargs):
        post_data = create_edit_issue()
        result = self.__submit('open', data=post_data)
        issue = get_key(result, 'issue')
        pprint_issue(issue)

    def close(self, number=None, **kwargs):
        validate_number(number, example="%s close 1" % get_prog())
        result = self.__submit('close', number)
        issue = get_key(result, 'issue')
        pprint_issue(issue)

    def reopen(self, number=None, **kwargs):
        validate_number(number, example="%s open 1" % get_prog())
        result = self.__submit('reopen', number)
        issue = get_key(result, 'issue')
        pprint_issue(issue)

    def edit(self, number=None, **kwargs):
        validate_number(number, example="%s edit 1" % get_prog())
        gh_issue = self.__get_issue(number)
        output = {'title': gh_issue['title'], 'body': gh_issue['body']}
        post_data = create_edit_issue(gh_issue)
        if post_data['title'] == output['title'] and \
                post_data['body'].splitlines() == output['body'].splitlines():
            print "no changes found"
            sys.exit(1)
        result = self.__submit('edit', number, data=post_data)
        issue = get_key(result, 'issue')
        pprint_issue(issue)

    def label(self, command, label, number=None, **kwargs):
        validate_number(number, example="%s label %s %s 1" % (get_prog(),
            command, label))
        if command not in ['add', 'remove']:
            msg = "label command should use either 'add' or 'remove'\n"\
                "example: %s label add %s %s" % (get_prog(), label, number)
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
        validate_number(number, example="%s comment 1" % get_prog())
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
            handle_error(result)
        else:
            return result


def main():
    usage = """usage: %prog command [args] [options]

Examples:
%prog list [-s open|closed|all]       show open, closed or all issues
                                    (default: open)
%prog [-s o|c|a] -v                   same as above, but with issue details
%prog                                 same as: %prog list
%prog -v                              same as: %prog list -v
%prog [-s o|c] -w                     show issues' GitHub page in web browser
                                    (default: open)
%prog show <nr>                       show issue <nr>
%prog show <nr> -v                    same as above, but with comments
%prog <nr>                            same as: %prog show <nr>
%prog <nr> -w                         show issue <nr>'s GitHub page in web
                                    browser
%prog open (o)                        create a new issue (with $EDITOR)
%prog close (c) <nr>                  close issue <nr>
%prog open (o) <nr>                   reopen issue <nr>
%prog edit (e) <nr>                   edit issue <nr> (with $EDITOR)
%prog label add (al) <label> <nr>     add <label> to issue <nr>
%prog label remove (rl) <label> <nr>  remove <label> from issue <nr>
%prog search (s) <term>               search for <term> (default: open)
%prog s <term> [-s o|c] -v            same as above, but with details
%prog s <term> -s closed              only search in closed issues
%prog comment (m) <nr>                create a comment for issue <nr>
                                    (with $EDITOR)
%prog -r <user>/<repo>                specify a repository (can be used for
                                    all commands)
%prog -r <repo>                       specify a repository (gets user from
                                    global git config)"""

    description = """Description:
command-line interface to GitHub's Issues API (v2)"""

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
      default=False, help="show issue details (only for show, list and "\
        "search commands) [default: False]")
    parser.add_option("-s", "--state", action="store", dest="state",
        type='choice', choices=['o', 'open', 'c', 'closed', 'a', 'all'],
        default='open', help="specify state (only for list and search "\
        "(except `all`) commands) choices are: open (o), closed (c), all "\
        "(a) [default: open]")
    parser.add_option("-r", "--repo", "--repository", action="store",
        dest="repo", help="specify a repository (format: "\
            "`user/repo` or just `repo` (latter will get the user from the "\
            "global git config))")
    parser.add_option("-w", "--web", "--webbrowser", action="store_true",
        dest="webbrowser", default=False, help="show issue(s) GitHub page "\
        "in web browser (only for list and show commands) [default: False]")
    parser.add_option("-V", "--version", action="store_true",
        dest="show_version", default=False,
        help="show program's version number and exit")

    class CustomValues:
        pass
    (options, args) = parser.parse_args(values=CustomValues)

    kwargs = dict([(k, v) for k, v in options.__dict__.items() \
        if not k.startswith("__")])
    if kwargs.get('show_version'):
        print("ghi %s" % get_version('short'))
        sys.exit(0)

    if kwargs.get('state'):
        kwargs['state'] = {'o': 'open', 'c': 'closed', 'a': 'all'}.get(
            kwargs['state'], kwargs['state'])

    if args:
        cmd = args[0]
        try:
            nr = str(int(cmd))
            if cmd == nr:
                cmd = 'show'
                args = (cmd, nr)
        except:
            pass
    else:
        cmd = 'list' # default command

    if cmd == 'search':
        search_term = " ".join(args[1:])
        args = (args[0], search_term)

    # handle command aliases
    cmd = {'o': 'open', 'c': 'close', 'e': 'edit', 'm': 'comment',
        's': 'search'}.get(cmd, cmd)
    if cmd == 'open' and len(args) > 1:
        cmd = 'reopen'
    if cmd == 'al' or cmd == 'rl':
        alias = cmd
        cmd = 'label'
        args_list = [cmd, {'a': 'add', 'r': 'remove'}[alias[0]]]
        args_list.extend(args[1:])
        args = tuple(args_list)

    try:
        repository = kwargs.get('repo')
        if repository:
            user, repo = get_remote_info_from_option(repository)
        else:
            user, repo = get_remote_info()
        commands = Commands(user, repo)
        getattr(commands, cmd)(*args[1:], **kwargs)
    except AttributeError:
        return "error: command '%s' not implemented" % cmd
    except Exception, info:
        return "error: %s" % info

if __name__ == '__main__':
    main()
