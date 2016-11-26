import unittest
from ded.DataProvider import DataProvider
from ded.Recipe import Recipe

class TestDataProvider(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_modules(self):
        data_provider = DataProvider(config={"load_modules":False})
        data_provider.load_modules()
        
        self.assertEqual(len(data_provider.available_modules), len(data_provider.modules))
        # TODO: advanced checks

    def test_empty_build(self):
        dict = {
            "title": "Test recipe",
            "sources": []
        }
        recipe = Recipe.from_dict(dict)

        provider = DataProvider()
        provider.build(recipe)
        # TODO: make proper tests
    
    def test_simple_build(self):
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

        provider = DataProvider()
        provider.build(recipe)

if __name__ == '__main__':
    unittest.main()