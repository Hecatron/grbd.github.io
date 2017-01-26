#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from conf.pelicanconf import *

SITEURL = 'http://grbd.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Social Section
SOCIAL = []
SOCIAL.append(('About Me', SITEURL + '/pages/profile/aboutme.html'))
#SOCIAL.append(('CV', SITEURL + '/pages/profile/cv.html'))
SOCIAL.append(('Github Personal', GITHUB_URL))
SOCIAL.append(('Github Company', GITHUB_URL2))
SOCIAL.append(('Projects', SITEURL + '/pages/profile/projects.html'))
#SOCIAL.append(('Linked In', "#TODO"))
SOCIAL = tuple(SOCIAL)


# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
