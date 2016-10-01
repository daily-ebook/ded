import subprocess
import os

from dominate.tags import *

class BookGenerator(object):
    def __init__(self, recipe):
        self.recipe = recipe

    def generate_html(self):
        book_title = self.recipe.pretty__title

        html = body(id="book")
        chapters = section(id="chapters")
        appendixes = section(id="appendixes")
        appendixes.add(h1("Appendix"))

        for chapter in (self.recipe.chapters or []):
            chapters.add(chapter.chapter.children)
            for appendix in chapter.appendixes:
                appendixes.add(appendix.appendix.children)

        html.add(chapters.children)
        html.add(appendixes.children)
        
        return str(html)

    def make_epub(self, html):
        current_path = os.path.dirname(os.path.realpath(__file__))

        tmp_dir = recipe.tmp_dir

        outfolder = recipe.outfolder
        filename = recipe.filename
        outfile = outfolder + filename

        with open('{0}/{1}.html'.format(tmp_dir, filename), 'w+') as f:
            f.write(html)

        with open('{0}/{1}-metadata.xml'.format(tmp_dir, filename), 'w+') as f:
            f.write("""<dc:title>{0}</dc:title>\n
                    <dc:creator opf:file-as="Daily Ebook" opf:role="aut"> 
                    Daily Ebook</dc:creator>""".format(recipe.pretty__title))

        subprocess.call(["pandoc",
                        "-S",
                        "-s",
                        "-o" + "{0}/{1}.epub".format(tmp_dir,filename) ,
                        "--epub-stylesheet={0}/epub-meta/style.css".format(current_path),
                        "--epub-metadata={0}/{1}-metadata.xml".format(tmp_dir,filename),
                        "{0}/{1}.html".format(tmp_dir,filename)])

        subprocess.call(["ebook-convert",
                        "{0}/{1}.epub".format(tmp_dir,filename),
                        "{0}.mobi".format(outfile),
                        "--input-profile=kindle"])

    def generate(self):
        html = generate_html()
        make_epub(html)

