# -*- coding: utf-8 -*-
import os
import shutil
from .base import BaseHelper


class PackageData(BaseHelper):
    """With debian package data"""
    files = [
        'source/format',
        'changelog',
        'clean',
        'compat',
        'control',
        'copyright',
        'docs',
        'rules',
    ]

    def __init__(self, path, context):
        super(PackageData, self).__init__()
        self._path = path
        self._context = context
        self.destination = os.path.join(self._path, 'debian')

    def _create_dirs(self):
        """Create all dirs"""
        os.makedirs(self.destination)
        self._sources_dir = os.path.join(self.destination, 'source')
        os.makedirs(self._sources_dir)

    def _render_file(self, path):
        """Render file"""
        template = self._env.get_template('{}.tmpl'.format(path))
        full_path = os.path.join(self.destination, path)
        with open(full_path, 'w') as out:
            out.write(template.render(**self._context.dict))

    def __enter__(self):
        """Create debian package data"""
        self._create_dirs()
        for name in self.files:
            self._render_file(name)

    def __exit__(self, *args, **kwargs):
        """Clean package data"""
        shutil.rmtree(self.destination)
