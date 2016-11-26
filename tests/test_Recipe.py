import unittest
from ded.Recipe import Recipe

class TestRecipe(unittest.TestCase):
    def setUp(self):
        pass

    def test_from_dict(self):
        dict = {
            "title": "Test recipe",
            "sources": []
        }
        recipe = Recipe.from_dict(dict)

        self.assertEqual(recipe.title, dict["title"])
        self.assertEqual(recipe.sources, dict["sources"])

    def test_pretty_title(self):
        recipe = Recipe()
        
        recipe.title = "Not a pretty title"
        self.assertEqual(recipe.pretty_title, "Not a pretty title")

        #recipe.title = "Today is "
        #self.assertEqual(recipe.pretty_title, "something")

if __name__ == '__main__':
    unittest.main()