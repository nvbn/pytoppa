import sys
import os
import setuptools
import yaml


class SetupParser(object):
    """Parser of setup.py"""

    def _patch_setuptools(self):
        """Patch setuptools"""
        setuptools.setup = self._store_args

    def _store_args(self, *args, **kwargs):
        self._data = kwargs

    def parse(self):
        """Parse setup.py"""
        self._patch_setuptools()
        sys.path.insert(0, os.getcwd())
        import setup
        return self._data


def main():
    SetupParser().parse()


if __name__ == '__main__':
    main()
