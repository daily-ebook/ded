import subprocess
import os

from dominate.tags import *

def generate_html(recipe):
    book_title = recipe.get("title")
    
    html = body(id="book")
    chapters = section(id="chapters")
    appendixes = section(id="appendixes")
    appendixes.add(h1("Appendix"))

    for chapter in (recipe.get("chapters", [])):
        chapters.add(chapter.chapter.children)
        for appendix in chapter.appendixes:
            appendixes.add(appendix.appendix.children)

    html.add(chapters.children)
    html.add(appendixes.children)

    return str(html)

def make_epub(html, recipe):
    current_path = os.path.dirname(os.path.realpath(__file__))
    
    tmp_dir = recipe.get("tmp_dir")

    outfolder = recipe.get("outfolder")
    filename = recipe.get("filename")
    outfile = outfolder + filename 
    
    with open('{0}/{1}.html'.format(tmp_dir,filename), 'w+') as f:
        f.write(html)

    with open('{0}/{1}-metadata.xml'.format(tmp_dir,filename), 'w+') as f:
        f.write('<dc:title>{0}</dc:title>\n<dc:creator opf:file-as="Andrew, Rachel" opf:role="aut">Rachel Andrew</dc:creator>'.format(recipe.get("title")))

    subprocess.call(["pandoc",
                    "-S",
                    "-s",
                    "-o" + "{0}/{1}.epub".format(tmp_dir,filename) , 
                    "--epub-stylesheet="+ current_path +"/epub-meta/style.css", 
                    "--epub-metadata={0}/{1}-metadata.xml".format(tmp_dir,filename),
                    "{0}/{1}.html".format(tmp_dir,filename)])

    subprocess.call(["ebook-convert", 
                    "{0}/{1}.epub".format(tmp_dir,filename), 
                    "{0}.mobi".format(outfile), 
                    "--input-profile=kindle"])

def generate_book(recipe):
    html = generate_html(recipe)
    make_epub(html, recipe)

