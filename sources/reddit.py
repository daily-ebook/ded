# reddit.com's sourcer
# subreddit: <subreddit>
# text: True or False
# summary: True or False
# comments: True or False
# commentsDepth: 1 (root)
# limit: n (defaults to 20)
import re


import requests
from newspaper import Article

from dominate.tags import *

from . import Chapter, Appendix

metadata = {
    "name": "reddit",
    "fullname": "Reddit",
    "description": "This source can parse subreddit, links and comments.",
    "options": []
}

def build(config):

    data = get_data(config)

    parse_content = config.get("content", False)
    parse_comments = config.get("comments", False)

    chapter = Chapter("reddit: /r/{0}".format(data.get("subreddit")),
                      "Sorting by {0}".format(data.get("sort_by")))

    if data.get("error") is None:

        posts = data.get("posts", [])

        for post in posts:
            if not post.get("stickied"):

                title = post.get("title")
                author = post.get("author") or "[deleted]"
                num_comments = post.get("num_comments")

                text_anchor = "reddit-{0}-text".format(post.get("id"))

                chapter.add(a(b(title), href="#{0}".format(text_anchor)))
                chapter.add(" ")
                chapter.add(small("({0})".format(post.get("domain"))))
                chapter.add(br())

                if parse_comments:
                    comments_anchor = "reddit-{0}-comments".format(post.get("id"))
                    chapter.add(a("{0} comments".format(num_comments), href="#"+comments_anchor))

                chapter.add(hr())
                #end of body, let's build appendix

                if parse_content:
                    appendix = Appendix(title, post.get("domain"), name=text_anchor)

                    if post.get("is_self"):
                        appendix.add(post.get("selftext") or "<This selfpost has no selftext>")
                    else:
                        if post.get("error") is None:
                            content_type = post.get("content_type")
                            if is_static_image(content_type):
                                appendix.add(img(src=post.get("url")))
                            elif is_unsupported(content_type):
                                appendix.add(p("Url File Format not supported"))
                            else:
                                article = post["article"]

                                if article.top_image:
                                    appendix.add(img(src=article.top_image))
                                appendix.add(p(article.text))
                        else:
                            chapter.add(p(post.get("error")))

                    chapter.add_appendix(appendix)

                if parse_comments:
                    if len(title) > 64:
                        title = "Comments for '{0}'".format(title[:61] + '...')

                    subtitle = "{0} comments".format(num_comments)
                    appendix = Appendix(title, subtitle, name=comments_anchor)
                    appendix.add("There should be comments here.")
                    chapter.add_appendix(appendix)
    else:
        chapter.add(p("API Status Code not 200"))

    return chapter

def get_data(config):
    data = {}
    subreddit = data["subreddit"] = config.get("subreddit", "all")
    sort_by = data["sort_by"] = config.get("sort_by", "hot")
    limit = data["limit"] = config.get("limit", 20)

    parse_content = config.get("content", False)
    summary = config.get("summary", False)

    parse_comments = config.get("comments", False)
    comments_limit = config.get("comments_limit", 20)
    comments_depth = config.get("comments_depth", 2)

    headers = {'user-agent': 'daily-epub by /u/cris9696'}
    url = "https://www.reddit.com/r/{0}/{1}.json".format(subreddit, sort_by)
    payload = {'limit': limit}
    subreddit_request = requests.get(url, headers=headers, params=payload)

    data["posts"] = []

    if subreddit_request.status_code == 200:
        json = subreddit_request.json()

        posts = json["data"]["children"]
        for post in posts:
            post = post.get("data")

            if parse_content:
                if post.get("is_self"):
                    pass
                else:
                    url = post["url"] = fix_url(post.get("url"))

                    #for content type
                    r_head = requests.head(url,
                                           headers=headers,
                                           allow_redirects=True)

                    if r_head.status_code == 200:
                        content_type = post["content_type"] = r_head.headers["Content-Type"]
                        if is_static_image(content_type) or is_unsupported(content_type):
                            pass
                        else:
                            article = Article(url)
                            article.download()
                            article.parse()

                            post["article"] = article
                    else:
                        post["error"] = "{0}: Error Code {1}".format(url, r_head.status_code)

            if parse_comments:
                comments_url = "https://www.reddit.com/comments/{1}.json".format(post.get("id"))
                comments_payload = {"limit": comments_limit, "depth": comments_depth}
                comments_request = requests.get(comments_url, headers=headers, params=comments_payload)

                data["comments"] = []

                if comments_request.status_code == 200:
                    comments = comments_request.json()
                    #TODO: finish comment parsing

            data["posts"].append(post)
    else:
        data["error"] = "{0}: Error Code {1}".format(url, r_head.status_code)

    return data

def is_unsupported(content_type):
    return content_type.startswith("video/") or content_type == "image/gif" or content_type.startswith("application/")

def is_static_image(content_type):
    return content_type.startswith("image/") and content_type != "image/gif"

def fix_url(url):
    if "imgur.com" in url:
        if "i.imgur.com" not in url:
            url = url.replace("imgur.com", "i.imgur.com")
            url = url.replace("/gallery", "")
            if re.search(r"\.[a-zA-Z\d]+$", url) is None:
                url = url + ".png"
            url = url.replace(".gifv", ".gif")
    return url
