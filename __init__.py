from . import utils
from . import book_generator

sources = utils.import_sources()
sources_metadata = utils.get_sources_metadata(sources)

def generate_book_from_recipe(recipe, task=None):
    recipe = utils.fix_recipe(recipe)

    utils.setup_user_space(recipe)

    recipe["chapters"] = []

    for i, reciped_source in enumerate(recipe.get("sources")):
        reciped_source_name = reciped_source.get("source")
        source = sources.get(reciped_source_name, None)
        if source:
            utils.update_state(task, state="PROGRESS", meta={'status': 'Building {0}'.format(reciped_source_name)})
            chapter = source.build(reciped_source.get("settings") or {})
            recipe.get("chapters").append(chapter)

    utils.update_state(task, state="PROGRESS", meta={'status': 'Generating e-book'})

    book_generator.generate_book(recipe)
    return True