import sys
from .base import BaseHelper


class ImportScope(BaseHelper):
    """Remove all new imports after finish"""

    def __enter__(self):
        self._modules = sys.modules.keys()

    def __exit__(self, *args, **kwargs):
        """Unload all loaded"""
        for module in sys.modules.keys():
            if module not in self._modules:
                del sys.modules[module]
