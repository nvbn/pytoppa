import sys
import os
import setuptools
from .exceptions import ParsingError


class SetupParser(object):
    """Parser of setup.py"""

    def _patch_setuptools(self):
        """Patch setuptools"""
        setuptools.setup = self._store_args

    def _store_args(self, *args, **kwargs):
        """Store arguments to setup"""
        self._data = kwargs

    def _check_exists(self, path):
        """Check setup.py exists"""
        setup_path = os.path.join(path, 'setup.py')
        if not os.path.exists(setup_path):
            raise ParsingError('setup.py not found')

    def parse(self, path):
        """Parse setup.py"""
        self._check_exists(path)
        self._patch_setuptools()
        sys.path.insert(0, path)
        import setup
        return self._data