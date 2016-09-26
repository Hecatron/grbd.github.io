#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from pelican.utils import path_to_url, get_relative_path

AUTHOR = 'Grbd'
SITENAME = 'The Grbd Blog'
SITEURL = 'http://localhost/MainBlog'
RELATIVE_URLS = True
USE_FOLDER_AS_CATEGORY = True
DISPLAY_CATEGORIES_ON_MENU = True
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
STATIC_PATHS = ['static', 'images']

# Map Static files to different paths
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/icons/omega.ico': {'path': 'favicon.ico'}
}

# Used for Development
LOAD_CONTENT_CACHE = False

#SITELOGO = 'images/logos/tachikoma3.png'
BANNER = "images/backdrops/backdrop1.jpg"
BANNER_ALL_PAGES = "True"
DEFAULT_PAGINATION = 10

#THEME = "themes/pelican-bootstrap3-lovers"
#BOOTSTRAP_THEME = "lovers"

THEME = "themes/pelican-bootstrap3.modv2"
#BOOTSTRAP_THEME = "cerulean"
#BOOTSTRAP_THEME = "cosmo"
BOOTSTRAP_THEME = "cyborg"
#BOOTSTRAP_THEME = "flatly"
#BOOTSTRAP_THEME = "slate"
#BOOTSTRAP_THEME = "darkly"
#BOOTSTRAP_FLUID = "True"

# Personal Info
GITHUB_URL = "https://github.com/grbd"
GITHUB_URL2 = "https://github.com/ASoftTech"

PATH = 'content'
TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social Section
SOCIAL = []
SOCIAL.append(('About Me', SITEURL + '/pages/profile/aboutme.html'))
SOCIAL.append(('CV', SITEURL + '/pages/profile/cv.html'))
SOCIAL.append(('Github Personal', GITHUB_URL))
SOCIAL.append(('Github Company', GITHUB_URL2))
#SOCIAL.append(('Linked In', "#TODO"))
SOCIAL = tuple(SOCIAL)

# Links Section
LINKS = []
#LINKS.append(('CV', SITEURL + '/pages/profile/cv.html'))
LINKS.append(('Manchester Hacspace', 'https://hacman.org.uk/'))
LINKS = tuple(LINKS)


# todo use plugin instead
# default value is ('index', 'tags', 'categories', 'archives')
# so we just add a 'sitemap' for the generation of sitemap.xml
#DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives', 'sitemap')
#SITEMAP_SAVE_AS = 'sitemap.xml'