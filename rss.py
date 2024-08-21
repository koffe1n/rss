import feedparser
import ssl
from termcolor import cprint

# url = "https://news.ru/rss/category/post/economics/"

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def getRssTitle(url):
    feed = feedparser.parse(url)
    return feed.feed.title 

def getRssContent(url):
    feed = feedparser.parse(url)
    return feed

