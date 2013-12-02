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

    def _check_exists(self, path, file_name):
        """Check setup.py exists"""
        setup_path = os.path.join(path, file_name)
        if not os.path.exists(setup_path):
            raise ParsingError('setup.py not found')

    def parse(self, path, file_name='setup.py'):
        """Parse setup.py"""
        self._check_exists(path, file_name)
        self._patch_setuptools()
        sys.path.insert(0, path)
        setup = __import__(file_name[:-3])
        reload(setup)
        return self._data