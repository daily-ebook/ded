from .exceptions import BadConfigException

from datetime import datetime 
import glob
import importlib
import os 

current_path = os.path.dirname(os.path.realpath(__file__))

def fix_config(config):
  config["tmp_dir"] = config.get("tmp_dir", "/tmp/")

  if False:
    raise BadConfigException("This should never happen")
  return config
  
def import_modules(folder, modules=None):
  loadedModules = []
  for module in modules:
    try:
      s = importlib.import_module(folder + "." + module, "ded")
      loadedModules.append(s)
    except Exception as e:
      print(e)
      print("Module not found")

  return loadedModules

def make_title(title):
  d = datetime.now()  
  title = d.strftime(title)
  return title

def get_sources_metadata():
  metadatas = []

  modules = glob.glob(current_path + "/sources/*.py")

  modules.remove(current_path + "/sources/__init__.py")

  for module in modules:
    module = module.replace(".py","").replace(current_path + "/sources/", "")
    try:
      s = importlib.import_module(".sources." + module, "ded")
      metadatas.append(s.metadata)
    except Exception as e:
      print(e)

  return metadatas

def update_state(task, **kwargs):
  if task:
    task.update_state(state='PROGRESS', **kwargs)

