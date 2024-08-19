import feedparser
import ssl

# url = "https://news.ru/rss/category/post/economics/"

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def getRssContent(url):
    feed = feedparser.parse(url)
    for i in feed.entries:
        print(i.id)
        print(i.title)
    return "%s %s" % (feed.entries[0].id, feed.entries[0].title)

# getRssContent(url)

