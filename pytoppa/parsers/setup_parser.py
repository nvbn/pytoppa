import sys
import setuptools


class SetupParser(object):
    """Parser of setup.py"""

    def _patch_setuptools(self):
        """Patch setuptools"""
        setuptools.setup = self._store_args

    def _store_args(self, *args, **kwargs):
        """Store arguments to setup"""
        self._data = kwargs

    def parse(self, path):
        """Parse setup.py"""
        self._patch_setuptools()
        sys.path.insert(0, path)
        import setup
        return self._data