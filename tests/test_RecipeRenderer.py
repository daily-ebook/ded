import unittest
from ded.Recipe import Recipe
from ded.RecipeRenderer import RecipeRenderer
from ded.sources import Chapter, Appendix

class TestRecipeRenderer(unittest.TestCase):
    def setUp(self):
        pass

    def test_render_dummy_html(self):
        dict = {
            "title": "Test recipe",
            "sources": []
        }
        recipe = Recipe.from_dict(dict)

        chapter = Chapter("Test Chapter Title",
            "Test Chapter Subtitle")
        appendix = Appendix("Test Appendix Title", "Test Appendix Subtitle", chapter.id)
        chapter.add_appendix(appendix)
        recipe.add_chapter(chapter)

        renderer = RecipeRenderer()
        renderer.render_html(recipe)
        # TODO: advanced checks
    
    def test_render_dummy_html(self):
        dict = {
            "title": "Test recipe",
            "sources": [
                {
                    "name": "reddit",
                    "config": {
                        "subreddit": "italy",
                        "limit": 20
                    }
                }
            ]
        }
        recipe = Recipe.from_dict(dict)
        recipe.build()

        renderer = RecipeRenderer()
        renderer.render_html(recipe)

        print(recipe.html)

if __name__ == '__main__':
    unittest.main()