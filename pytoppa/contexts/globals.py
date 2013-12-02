from ..parsers.git_parser import GitParser
from ..parsers.setup_parser import SetupParser
from ..parsers.config_parser import ConfigParser
from .base import BaseContext


class GlobalContext(BaseContext):
    """Global context"""

    def __init__(self, path):
        super(GlobalContext, self).__init__()
        self._path = path
        self._fill()

    def _fill(self):
        """Gill context"""
        self.dict['setup_py_kwargs'] = self._get_package_data()
        self.dict.update(self.dict['setup_py_kwargs'])
        self.dict.update(self._get_config_data())

    def update_changelog(self, path):
        """Update changelog"""
        self.dict['changelog'] = list(self._create_changelog(path))

    def _create_changelog(self, path):
        """Create changelog"""
        for version, logs, date in GitParser().parse(path)[::-1]:
            yield {
                'version': version,
                'logs': logs,
                'date': date,
            }

    def _get_package_data(self):
        """Get package data"""
        data = SetupParser().parse(self._path)
        data['name'] = data['name'].replace('_', '-')
        return data

    def _get_config_data(self):
        """Get config data"""
        return ConfigParser().parse(self._path)
