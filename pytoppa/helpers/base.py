from jinja2 import Environment, PackageLoader


class BaseHelper(object):
    """Base helper"""

    def __init__(self):
        self._env = Environment(loader=PackageLoader('pytoppa'))
