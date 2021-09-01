## check-gmail.py -- A command line util to check GMail -*- Python -*-
## modified to display mailbox summary for conky

# ======================================================================
# Copyright (C) 2006 Baishampayan Ghose <b.ghose@ubuntu.com>
# Modified 2008 Hunter Loftis <hbloftis@uncc.edu>
# Time-stamp: Mon Jul 31, 2006 20:45+0530
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

import sys
import urllib.request             # For BasicHTTPAuthentication
import feedparser         # For parsing the feed
from textwrap import wrap

uname = sys.argv[1]
password = sys.argv[2]
maxlen = sys.argv[3]
	
def auth(user, passwd):
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='mail.google.com',
        uri='https://mail.google.com',
        user=user,
        passwd=passwd
    )
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    feed = urllib.request.urlopen('https://mail.google.com/mail/feed/atom')
    return feed.read()


def readmail(feed, maxlen):
	'''Parse the Atom feed and print a summary'''
	atom = feedparser.parse(feed)
	print ('${color} %s new email(s)\n' % (len(atom.entries)))
	for i in range(min(len(atom.entries), maxlen)):
#uncomment the following line if you want to show the name of the sender
		print ('${alignr}${color}%s' % atom.entries[i].author_detail.name)
		print ('${alignr}${color}%s\n' % atom.entries[i].title)
	if len(atom.entries) > maxlen:
		print ('${color}more...')

if __name__ == "__main__":
    f = auth(uname, password)  # Do auth and then get the feed
    readmail(f, int(maxlen)) # Let the feed be chewed by feedparser
