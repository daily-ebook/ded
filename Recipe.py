class Recipe(object):
    def __init__(self, dict):
        self.dict = dict

    @property
    def pretty_title(self):
        d = datetime.now()
        title = d.strftime(self.title)
        
        return title

    def __getattr__(self, key):
        return self.dict.get(key)

    def __setattr__(self, key, value):
        self.dict[key] = value
