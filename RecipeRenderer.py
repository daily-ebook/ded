from dominate.tags import *

class RecipeRenderer(object):
    def __init__(self):
        self.output_type = "html"

    def render(self, recipe):
        if(self.output_type == "html"):
            self.render_html(recipe)
            
    def render_html(self, recipe):
        html = body(id="book")
        
        chapters = section(id="chapters")
        appendixes = section(id="appendixes")
        appendixes.add(h1("Appendix"))

        for chapter in recipe.chapters:
            chapters.add(chapter.chapter)
            for appendix in chapter.appendixes:
                appendixes.add(appendix.appendix)

        html.add(chapters)
        html.add(appendixes)
        
        recipe.html = str(html)