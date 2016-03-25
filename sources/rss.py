
import requests 
from newspaper import Article
import feedparser

def build(config):
    link = config.get("source")
    limit = config.get("limit", 10)

    feed = feedparser.parse(link)

    source = {}
    source["title"] = feed['feed']["title"]
    source["subtitle"] = feed['feed']["subtitle"]

    source["body"] = ""
    source["appendixes"] = []

    for i in range(0, min(limit, len(feed["entries"])) ):
        entry = feed["entries"][i]
        title = entry["title"]
        link = entry["link"]
        textAnchor = "rss-" + link
        source["body"] += "**{0}**\n\n".format(title)
        source["body"] += "-----\n\n"

        appendix = {}
        appendix["title"] = title
        article = Article(link)
        article.download()
        article.parse()
        appendix["body"] = article.text
        source["appendixes"].append(appendix)

    return source