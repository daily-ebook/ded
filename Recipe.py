from ded.Exceptions import BadRecipeException
from ded.DataProvider import DataProvider
from ded.RecipeRenderer import RecipeRenderer

from datetime import datetime

class Recipe(object):
    def __init__(self):
        self.title = ""
        self.sources = []
        self.chapters = []

    @staticmethod
    def from_dict(dict):
        recipe = Recipe()
        recipe.title = dict.get("title")
        recipe.sources = dict.get("sources")
        return recipe

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def check(self):
        if False:
            raise BadRecipeException("This should never happen")
        return True

    def build(self):
        provider = DataProvider()
        provider.build(self)

    def render(self):
        renderer = RecipeRenderer()
        renderer.render(self)

    @property
    def pretty_title(self):
        d = datetime.now()
        title = d.strftime(self.title)

        return title