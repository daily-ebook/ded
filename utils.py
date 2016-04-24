from .exceptions import BadConfigException

from datetime import datetime 
import glob
import importlib
import os 

current_path = os.path.dirname(os.path.realpath(__file__))

def setup_user_space(recipe):
  outfolder = recipe.get("outfolder")
  tmp_dir = recipe.get("tmp_dir")

  if not os.path.exists(outfolder):
    os.makedirs(outfolder)

  if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

def fix_recipe(recipe):
  d = datetime.now()  
  folder = "/tmp/books/"+d.strftime("%H%M%S")
  recipe["tmp_dir"] = recipe.get("tmp_dir", folder)

  if False:
    raise BadRecipeException("This should never happen")
  return recipe

#FIXME: HACK: this function sucks  
def import_sources():
  folder = "sources"
  import_path = "{0}/{1}".format(current_path, folder)

  modules = glob.glob("{0}/*.py".format(import_path))
  modules.remove("{0}/__init__.py".format(import_path))
  loaded_modules = []
  for module in modules:
    module = module.replace(".py","").replace(import_path + "/", "")
    try:
      module = importlib.import_module(".{0}.{1}".format(folder, module), "ded")
      loaded_modules.append(module)
    except Exception as e:
      print(e)
  return loaded_modules

def make_title(title):
  d = datetime.now()  
  title = d.strftime(title)
  return title

def get_sources_metadata(sources):
  metadatas = []

  for source in sources:
    metadatas.append(source.metadata)
  return metadatas

def update_state(task, **kwargs):
  if task:
    task.update_state(state='PROGRESS', **kwargs)

