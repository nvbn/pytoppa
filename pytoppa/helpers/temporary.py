import uuid
import os
import shutil


class TemporaryDirectory(object):
    """With temporary directory"""

    def __init__(self, path, context):
        self._context = context
        self._project_path = path
        self._path = os.path.join(
            '/tmp', 'pytoppa_{}'.format(uuid.uuid4().hex),
        )
        self.destination = os.path.join(self._path, context['name'])

    def __enter__(self):
        """Create temporary directory"""
        os.makedirs(self._path)
        shutil.copytree(self._project_path, self.destination)

    def __exit__(self, *args, **kwargs):
        """Clean temporary directory"""
        shutil.rmtree(self._path)
