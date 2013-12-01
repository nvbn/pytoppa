class BaseContext(object):
    """Base context"""

    def __init__(self):
        self.dict = {}

    def __getitem__(self, item):
        return self.dict[item]
