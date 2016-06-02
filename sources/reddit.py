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
  
  parseContent = config.get("content", False)
  summary = config.get("summary", False)
  
  parseComments = config.get("comments", False)
  commentsDepth = config.get("commentsDepth", 1)

  chapter = Chapter("reddit: /r/{0}".format(subreddit), "Sorting by {0}".format(sort))

  headers = {'user-agent': 'daily-epub by /u/cris9696'}

  url = "https://www.reddit.com/r/{0}/{1}.json".format(subreddit,sort)
  payload = {'limit': limit}
  r = requests.get(url, headers=headers, params=payload)

  if r.status_code == 200:
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

        chapter.add( a(b(title), href="#"+textAnchor) ) 
        chapter.add( " " )
        chapter.add( small("({0})".format(post.get("domain"))) )
        chapter.add( br() )

        if parseComments:
          chapter.add(a("{0} comments".format(num_comments),href="#"+commentsAnchor))

        chapter.add(hr())
        #end of body, let's build appendix

        if parseContent:
          appendix = Appendix(title, post.get("domain"), name=textAnchor)

          if post.get("is_self"):
            appendix.add(post.get("selftext") or "<This selfpost has no selftext>")
          else:
            url = post.get("url")
            r_head = requests.head(url, headers=headers) #for content type

            if r_head.status_code == 200:
              content_type = r_head.headers["Content-Type"]
              if content_type.startswith("image/") and content_type != "image/gif":
                appendix.add( img(src=url) )

              elif content_type.startswith("video/") or content_type == "image/gif" or content_type.startswith("application/"):
                appendix.add( p("Url File Format not supported") ) 
              
              else:
                article = Article(url)
                article.download()
                article.parse()

                if article.top_image:
                  appendix.add( img(src=article.top_image) )
                appendix.add( p(article.text) ) 

            else:
              chapter.add( p("API Status Code not 200") )

          chapter.addAppendix(appendix)

        if parseComments:
          if len(title) > 64:
            title = "Comments for '{0}'".format(title[:61] + '...')

          subtitle = "{0} comments".format(num_comments)
          appendix = Appendix(title, subtitle, name=commentsAnchor)
          appendix.add( "There should be comments here." )
          chapter.addAppendix(appendix)
  else:
    chapter.add( p("API Status Code not 200") )

  return chapter