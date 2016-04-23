import subprocess
import os

from dominate.tags import *

def generate_html(recipe):
  book_title = recipe.get("title")
  html = div(id="book")
  chapters = div(id="chapters")
  appendixes = div(id="appendixes")

  for chapter in (recipe.get("chapters", [])):
    chapters.add(chapter.chapter)
    for appendix in chapter.appendixes:
      appendixes.add(appendix.appendix)

  html.add(chapters)
  html.add(appendixes)

  return str(html)

def make_epub(html, recipe):
  current_path = os.path.dirname(os.path.realpath(__file__))
  filename = recipe.get("filename")
  savepath = recipe.get("savepath", "./")
  outfile = savepath + filename 
  
  with open('/tmp/{0}.html'.format(filename), 'w+') as f:
    f.write(html)

  with open('/tmp/{0}-metadata.xml'.format(filename), 'w+') as f:
    f.write('<dc:title>{0}</dc:title>\n<dc:creator opf:file-as="Andrew, Rachel" opf:role="aut">Rachel Andrew</dc:creator>'.format(recipe.get("title")))

  print(html)
  subprocess.call(["pandoc",
                  "-S", 
                  "-o" + "/tmp/{0}.epub".format(filename) , 
                  "--epub-stylesheet="+ current_path +"/epub-meta/style.css", 
                  "--epub-metadata=/tmp/{0}-metadata.xml".format(filename),
                  "/tmp/{0}.html".format(filename)])

  subprocess.call(["ebook-convert", "/tmp/{0}.epub".format(filename), "{0}.mobi".format(outfile), "--input-profile=kindle"])

def generate_book(recipe):
  html = generate_html(recipe)
  make_epub(html, recipe)

