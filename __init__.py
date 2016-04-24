from . import utils
from . import book_generator

sources = utils.import_sources()
sources_metadata = utils.get_sources_metadata(sources)

def generate_book_from_recipe(recipe, task=None):
  recipe = utils.fix_recipe(recipe)

  utils.setup_user_space(recipe)

  recipe["title"] = utils.make_title(recipe.get("title") or "Daily Epub")
  recipe["chapters"] = []

  utils.update_state(task, meta={'status': 'Importing sources'})

  #XXX: Improve this for loop
  for i, reciped_source in enumerate(recipe.get("sources")):
    reciped_source_name = reciped_source.get("source")
    for source_generator in sources: 
      if source_generator.metadata.get("name") == reciped_source_name:
        chapter = source_generator.build(reciped_source.get("settings") or {})
        
        recipe.get("chapters").append(chapter)


  book_generator.generate_book(recipe)
  return True