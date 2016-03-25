import subprocess
import os

def generate_markdown_from_book(book, depth):
  md = ""
  mdApdx = "" 
  if depth==0: #book title
    md += "%{0}\n\n".format(book.get("title"))
  else:
    md += "{0} {1}\n\n".format("#"*depth, book.get("title"))
    md += "<p class='subtitle'>{0}</p>\n\n".format(book.get("subtitle", ""))
    md += "{0}\n\n".format(book.get("body", ""))

  for chapter in (book.get("chapters", [])):
    md += generate_markdown_from_book(chapter, depth+1)[0]

    for appendix in (chapter.get("appendixes", [])):
      mdApdx += generate_markdown_from_book(appendix, max(depth+1,2))[0]

  return md, mdApdx

def make_epub(md, book, config):
  current_path = os.path.dirname(os.path.realpath(__file__))
  filename = config.get("filename")
  savepath = config.get("savepath", "./")
  outfile = savepath + filename 
  

  with open('/tmp/{0}.md'.format(filename), 'w+') as f:
    f.write(md)

  with open('/tmp/{0}-metadata.txt'.format(filename), 'w+') as f:
    f.write("""
      ---
      title: {0}
      author: daily-epub
      ---""".format(book.get("title")))
    
  subprocess.call(["pandoc","-S", "-o" + "/tmp/{0}.epub".format(filename) , "--epub-metadata=" + '/tmp/{0}-metadata.txt'.format(filename), "--epub-stylesheet="+ current_path +"/epub-meta/style.css", "/tmp/{0}.md".format(filename)])
  subprocess.call(["ebook-convert", "/tmp/{0}.epub".format(filename), "{0}.mobi".format(outfile), "--input-profile=kindle"])

def prepare_markdown(md, mdApdx):
  mdApdx = "\n\n#Content\n\n{0}".format(mdApdx)
  return md + "\n\n" + mdApdx

def generate_book(book, config):
  md, mdApdx = generate_markdown_from_book(book, 0)
  md = prepare_markdown(md, mdApdx)
  make_epub(md, book, config)

