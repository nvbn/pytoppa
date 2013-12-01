from copy import copy
from .base import BaseContext


class ReleaseContext(BaseContext):
    """Per-release context"""

    def __init__(self, global_context, release):
        super(ReleaseContext, self).__init__()
        self._global = global_context
        self._release = release
        self._fill()

    def _fill(self):
        """Fill context"""
        self.dict = copy(self._global.dict)
        self.dict['release'] = self._release
