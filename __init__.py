from . import utils
from . import book_generator

import yaml

"""if __name__ == "__main__":
    with open("recipe.yaml", 'r') as file:
        config = yaml.load(file)
        generate_book_from_config(config)""" 

def generate_book_from_config(config, task=None):
  config = utils.fix_config(config)

  book = {}
  book["title"] = utils.make_title(config.get("title") or "Daily Epub")
  book["chapters"] = []

  utils.update_state(task, meta={'status': 'Importing sources'})
  sources = utils.import_modules(".sources", config.get("sources"))
  for i, source in enumerate(config.get("sources")):
    chapter = sources[i].build(config.get("settings")[i][source])
    #checkChapter(chapter)
    book.get("chapters").append(chapter)

  book_generator.generate_book(book, config)
  return True