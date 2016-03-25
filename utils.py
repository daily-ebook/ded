from .exceptions import BadConfigException

from datetime import datetime 
import glob
import importlib

def fix_config(config):
  config["tmp_dir"] = config.get("tmp_dir", "/tmp/")

  if False:
    raise BadConfigException("This should never happen")
  return config
  
def import_modules(folder, modules):
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

def get_sources_metadata(folder):
  generators = []

  modules = glob.glob("folder/*.py")
  modules.remove("__init__.py")

  for module in modules:
    module = module.replace(".py","")
    print(module)
    try:
      s = __import__("{0}.{1}".format(folder,module), fromlist=[''])
      generators.append(s.meta)
    except Exception as e:
      print(e)

  return generators

def update_state(task, **kwargs):
  if task:
    task.update_state(state='PROGRESS', **kwargs)

