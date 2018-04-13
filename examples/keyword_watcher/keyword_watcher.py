#!/usr/bin/env python2

# Requirements:
#   subprocess32 python package
#   nodejs
#       puppeteer npm package
#       sleep npm package

CREDS_FILENAME = 'creds.json'

import json, os, re, sys, time
sys.path.append(os.getcwd())
from redditlib import *

mydir, _ = os.path.split(os.path.abspath(sys.argv[0]))

def preflight():
    try:
        import subprocess32 as subprocess
    except ImportError:
        print >>sys.stderr, "This example requires the subprocess32 python package"
        sys.exit(1)

    try:
        import praw
    except ImportError:
        print >>sys.stderr, "This example requires the praw python package"
        sys.exit(1)

    if not os.path.exists(CREDS_FILENAME):
        print >>sys.stderr, 'This example requires a {} file in the current directory with your Reddit API credentials.'.format(CREDS_FILENAME)
        print >>sys.stderr, 'Format:'
        print >>sys.stderr, '{'
        print >>sys.stderr, '  "client_id": "xxxxxx",'
        print >>sys.stderr, '  "client_secret": "xxxxxx",'
        print >>sys.stderr, '  "user_agent": "xxxxxx",'
        print >>sys.stderr, '}'
        print >>sys.stderr, 'See http://praw.readthedocs.io/en/latest/getting_started/quick_start.html for more info about these values.'
        sys.exit(1)

    try:
        subprocess.call(['node','-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print >>sys.stderr, "This example requires nodejs to be installed"
        sys.exit(1)

    for npm_package in ('puppeteer', 'sleep'):
        rc = subprocess.call(['node','-e','require("{}")'.format(npm_package)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=mydir)
        if rc:
            print >>sys.stderr, "This example requires the {} npm package installed in the Python script's directory".format(npm_package)
            print >>sys.stderr, 'To install, cd to {} and run "npm install {}"'.format(mydir, npm_package)
            sys.exit(1)

    #phew, we're good to go now

preflight()

import subprocess32 as subprocess
import praw

with open(CREDS_FILENAME, 'r') as f:
    creds = json.load(f)

r = praw.Reddit(client_id = creds['client_id'],
                client_secret = creds['client_secret'],
                user_agent = creds['user_agent'])

if len(sys.argv) < 3:
    print >>sys.stderr, 'usage:'
    print >>sys.stderr, '    python2 {} <subreddit_name> <keyword_file>'.format(__file__)
    sys.exit(1)

jsonlog = JsonLog('kw_output.json', append=True)

sr_name = normalize_subreddit(sys.argv[1])
sr = r.subreddit(sr_name)

with open(sys.argv[2], 'r') as f:
    KEYWORDS = set([kw.strip() for kw in f])

if len(KEYWORDS) < 40:
    print 'watching /r/{} for the following keywords:'.format(sr.display_name)
    for kw in KEYWORDS:
        print '    ',kw
else:
    print 'watching /r/{} for {} keywords'.format(sr.display_name, len(KEYWORDS))

watcher = CommentKeywordWatcher(sr)
for kw in KEYWORDS:
    watcher.add_keyword(kw)

while True:
    for match in watcher.check():
        author = match.thing.author.name.encode('utf-8')
        body = match.thing.body.encode('utf-8')
        link = 'https://reddit.com' + match.thing.permalink.encode('utf-8')
    
        jsonlog.write({
            'author': author,
            'id': match.thing.id,
            'url': link,
            'keywords': match.keywords,
            'body': body,
        })

        for kw in match.keywords:
            body = re.sub('('+kw.lower()+')', '\x1b[35m\x1b[1m\\1\x1b[22m\x1b[0m', body, flags=re.I)

        print '---'
        print '/u/{}'.format(author)
        print link
        print
        print body
        print
        sys.stdout.flush()

        if not os.path.exists('screens'):
            print 'making screens directory'
            os.mkdir('screens')

        filename = os.path.join(os.getcwd(), 'screens', '{}.png'.format(match.thing.id))
        print 'saving to {}'.format(filename)
        try:
            rc = subprocess.call(['node', 'screenshot.js', link, filename], timeout = 15, cwd = mydir)
        except subprocess.TimeoutExpired as e:
            pass

        print 'submitting to archive.is'
        try:
            rc = subprocess.call(['node', 'archive.js', link + '?context=100'], timeout = 15, cwd = mydir)
        except subprocess.TimeoutExpired as e:
            pass

        subprocess.call(['killall','-9','chrome'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
