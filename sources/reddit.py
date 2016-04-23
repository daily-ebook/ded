# reddit.com's sourcer
# subreddit: <subreddit>
# text: True or False
# summary: True or False
# comments: True or False
# commentsDepth: 1 (root)
# limit: n (defaults to 20)
from . import Chapter, Appendix
from dominate.tags import *

import requests 
from newspaper import Article

metadata = {
  "name": "reddit",
  "fullname": "Reddit",
  "description": "This source will provide fake data, as a test.",
  "options": []
}

def build(config):
    subreddit = config.get("subreddit", "all")
    sort = config.get("sort", "hot")
    limit = config.get("limit", 20)
    text = config.get("text", False)
    comments = config.get("comments", False)
    summary = config.get("summary", False)
    commentsDepth = config.get("commentsDepth", 1)

    chapter = Chapter("reddit: /r/{0}".format(subreddit), "Sorting by {0}".format(sort))

    url = "https://www.reddit.com/r/{0}/{1}.json".format(subreddit,sort)
    payload = {'limit': limit}
    headers = {'user-agent': 'daily-epub by /u/cris9696'}
    r = requests.get(url, headers=headers, params=payload)
    json = r.json()
    

    posts = json["data"]["children"]
    for post in posts:
        post = post.get("data")
        if not post.get("stickied"):
            title = post.get("title")
            author = post.get("author") or "[deleted]"
            num_comments = post.get("num_comments")
            commentsAnchor = "#reddit-{0}-comments".format(post.get("id"))
            textAnchor = "#reddit-{0}-text".format(post.get("id"))

            chapter.add(b("{0}".format(title)))
            chapter.add(br())

            if text:
                if post.get("is_self"):
                    kind = "Self Text"
                else:
                    kind = "Link Text"

                chapter.add(a(kind,href=textAnchor))

            if comments:
                chapter.add(a("{0} comments".format(num_comments),href=commentsAnchor))

            chapter.add(hr())
            #end of body, let's build appendix

            if text:
                appendix = Appendix(title)

                if post.get("is_self"):
                    appendix.add(post.get("selftext") or "<Selfpost has no selftext>")
                else:
                    url = post.get("url")
                    article = Article(url)
                    article.download()
                    article.parse()
                    appendix.add(article.text) 

                chapter.addAppendix(appendix)


                """if comments:
                title = ("Comments for '{0}'".format((title[:61] + '...') if len(title) > 64 else title)
                subtitle = "{0} comments".format(num_comments)
                appendix = chapter.createAppendix(title, subtitle)
                appendix.add("There should be comments here.")
                chapter.addAppendix(appendix)"""
    return chapter