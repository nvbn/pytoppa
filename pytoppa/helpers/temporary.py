from copy import copy
from pprint import pformat
import uuid
import os
import shutil
from .base import BaseHelper


class TemporaryDirectory(BaseHelper):
    """With temporary directory"""

    def __init__(self, path, context):
        super(TemporaryDirectory, self).__init__()
        self._context = context
        self._project_path = path
        self._path = os.path.join(
            '/tmp', 'pytoppa_{}'.format(uuid.uuid4().hex),
        )
        self.destination = os.path.join(self._path, context['name'])

    def _prepare_data_files(self, data_files):
        """Replace share with /usr/share/"""
        for destination, files in data_files:
            if destination.find('share/') == 0:
                yield '/usr/{}'.format(destination), files
            else:
                yield destination, files

    def _create_setup_py(self):
        """Create setup.py"""
        template = self._env.get_template('setup.py.tmpl')
        context = copy(self._context['setup_py_kwargs'])
        context['install_requires'] = []
        context['data_files'] =\
            list(self._prepare_data_files(context.get('data_files', [])))
        path = os.path.join(self.destination, 'setup.py')
        with open(path, 'w') as setup_py:
            setup_py.write(template.render(data=pformat(context)))

    def __enter__(self):
        """Create temporary directory"""
        os.makedirs(self._path)
        shutil.copytree(
            self._project_path, self.destination,
            ignore=shutil.ignore_patterns('*.pyc'),
        )
        self._create_setup_py()
        return self

    def __exit__(self, *args, **kwargs):
        """Clean temporary directory"""
        shutil.rmtree(self._path)
