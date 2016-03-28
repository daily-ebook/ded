# reddit.com's sourcer
# subreddit: <subreddit>
# text: True or False
# summary: True or False
# comments: True or False
# commentsDepth: 1 (root)
# limit: n (defaults to 20)
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

    source = {}
    source["title"] = subreddit
    source["Subtitle"] = "Sorting by {0}".format(sort)

    source["body"] = ""
    source["appendixes"] = []
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
            commentsAnchor = "reddit-{0}-comments".format(post.get("id"))
            textAnchor = "reddit-{0}-text".format(post.get("id"))

            source["body"] += "**{0}**\n\n".format(title)

            strBody = ""
            if text:
                kind = "Link Text"
                if post.get("is_self"):
                    kind = "Self Text"
                strBody += "[{0}](#{1}) ".format(kind, textAnchor)

            if comments:
                strBody += "[{0} comments](#{1})".format(num_comments, commentsAnchor)

            source["body"] += "{0}\n\n".format(strBody)
            source["body"] += "-----\n\n"
            #end of body, let's build appendix

            if text:
                appendix = {}
                if post.get("is_self"):
                    appendix["title"] = title
                    appendix["body"] = post.get("selftext") or "<Selfpost has no selftext>"
                else:
                    appendix["title"] = title
                    url = post.get("url")
                    article = Article(url)
                    article.download()
                    article.parse()
                    appendix["body"] = article.text

                source["appendixes"].append(appendix)


            if comments:
                appendix = {}
                appendix["title"] = "Comments for '{0}'".format((title[:61] + '...') if len(title) > 64 else title)
                appendix["subtitle"] = "*{0}* comments".format(num_comments)
                appendix["body"] = "There should be comments here."
                source["appendixes"].append(appendix)

    return source