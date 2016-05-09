import os
import yaml
from .exceptions import ParsingError


class ConfigParser(object):
    """Parse config in yaml"""

    def _get_config_path(self, path):
        """Get config path"""
        with_yml = os.path.join(path, '.pytoppa.yml')
        with_yaml = os.path.join(path, '.pytoppa.yaml')
        if os.path.exists(with_yml):
            return with_yml
        elif os.path.exists(with_yaml):
            return with_yaml
        else:
            raise ParsingError('pytoppa config not found')

    def _fill_defaults(self, data):
        """Fill default values to config"""
        if 'section' not in data:
            data['section'] = 'python'
        if 'dependencies' not in data:
            data['dependencies'] = []
        data['build_dependencies'] = data.get('build-dependencies', [])
        return data

    def _validate(self, data):
        """Validate config"""
        if type(data['dependencies']) is not list:
            raise ParsingError('dependencies should be list')
        if 'releases' not in data:
            raise ParsingError('releases should be filled')
        if type(data['releases']) is not list:
            raise ParsingError('releases should be list')

    def parse(self, path):
        """Parse config in yaml"""
        with open(self._get_config_path(path)) as config_file:
            data = yaml.load(config_file.read())
        self._fill_defaults(data)
        self._validate(data)
        return data
