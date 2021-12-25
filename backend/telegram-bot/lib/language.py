import yaml


class Language(object):
    def __init__(self, code="en"):
        self.code = code
        self.load()

    def load(self):
        with open(f"language/{self.code}.yml") as fp:
            self.data = yaml.load(fp, Loader=yaml.BaseLoader)
