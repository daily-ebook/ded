from .exceptions import BadRecipeException

import importlib
import os

def setup_user_space(recipe):
    outfolder = recipe.outfolder
    tmp_dir = recipe.tmp_dir

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

def fix_recipe(recipe):
    recipe["title"] = make_ebook_title(recipe.get("title") or "Daily Epub")

    if False:
        raise BadRecipeException("This should never happen")

    return recipe

#https://github.com/WikiToLearn/texla/blob/master/texla/Parser/Blocks/__init__.py
def import_sources():
    not_import = ['__init__.py']
    loaded_modules = {}
    for moduleFile in os.listdir(os.path.dirname(__file__) + "/sources"):
        if moduleFile in not_import:
            continue
        if moduleFile.endswith('.py'):
            module = importlib.import_module('ded.sources.'+ moduleFile[:-3])
            loaded_modules[module.metadata["name"]] = module

    return loaded_modules

def get_sources_metadata(sources):
    metadatas = []
    for source_name, source in sources.items():
        metadatas.append(source.metadata)
    return metadatas

def update_state(task, **kwargs):
    if task:
        task.update_state(**kwargs)

