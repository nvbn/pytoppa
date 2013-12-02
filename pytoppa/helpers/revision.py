import shutil
import os
import subprocess
from .base import BaseHelper


class Revision(BaseHelper):
    """With revision"""

    def __init__(self, revision, path):
        super(Revision, self).__init__()
        self._revision = revision
        self._path = path
        self.destination = os.path.join(path, '..', revision)
        self.setup_py = os.path.join(self.destination, 'setup.py')

    def __enter__(self):
        """Copy current and checkout to revision"""
        shutil.copytree(self._path, self.destination)
        self._switch_to_revision()
        self._generate_setup_py()
        return self

    def _switch_to_revision(self):
        """Switch to revision"""
        subprocess.call(['git', 'stash'], cwd=self.destination)
        subprocess.call(
            ['git', 'checkout', self._revision],
            cwd=self.destination,
        )

    def _generate_setup_py(self):
        """Generate correct setup.py"""
        with open(self.setup_py) as setup_py:
            content = setup_py.read()
        template = self._env.get_template('revision_setup_py.tmpl')
        with open(self.setup_py, 'w') as setup_py:
            setup_py.write(template.render(content=content))

    def __exit__(self, *args, **kwargs):
        """Clean revision"""
        shutil.rmtree(self.destination)
