import importlib
from multiprocessing.pool import ThreadPool

class DataProvider(object):
    def __init__(self, config={}):
        self.available_modules = ["reddit", "rss"]
        self.modules = {}
        self.config = config

        if self.config.get("load_modules", True):
            self.load_modules()

    def load_modules(self):
        for module_file_name in self.available_modules:
            module = importlib.import_module('ded.sources.'+ module_file_name)
            self.modules[module.metadata["name"]] = module

    def build(self, recipe):
        if self.config.get("parallel", True):
            self.build_threading(recipe)
        else:
            pass
            #TODO self.build_sequential(recipe)

    def build_threading(self, recipe):
        pool = ThreadPool(processes=5)
        processes = []
        for i, source in enumerate(recipe.sources):
            process = pool.apply_async(self.modules[source.get("name")].build, (source.get("config", {}),))
            processes.append(process)

        for i, process in enumerate(processes):
            chapter = process.get();
            recipe.add_chapter(chapter)
