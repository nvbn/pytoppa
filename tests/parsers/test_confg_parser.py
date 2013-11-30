import sure
import os
from mock import MagicMock
from unittest import TestCase
from pytoppa.parsers.config_parser import ConfigParser
from pytoppa.parsers.exceptions import ParsingError
from ..base import FIXTURES_PATH


class ConfigParserCase(TestCase):
    """Case for pytoppa.yml parser"""

    def setUp(self):
        self._mock_config_path()

    def _mock_config_path(self):
        """Mock _get_config_path method"""
        self._orig_config_path = ConfigParser._get_config_path
        ConfigParser._get_config_path = MagicMock()

    def tearDown(self):
        ConfigParser._get_config_path = self._orig_config_path

    def test_parse_config(self):
        """Test parse config"""
        ConfigParser._get_config_path.return_value = os.path.join(
            FIXTURES_PATH, 'pytoppa.yml',
        )
        ConfigParser().parse('')['section'].should.be.equal('net')

    def test_parse_without_section(self):
        """Test parse without section"""
        ConfigParser._get_config_path.return_value = os.path.join(
            FIXTURES_PATH, 'pytoppa_without_section.yml',
        )
        ConfigParser().parse('')['section'].should.be.equal('python')

    def test_parse_without_deps(self):
        """Test parse without deps"""
        ConfigParser._get_config_path.return_value = os.path.join(
            FIXTURES_PATH, 'pytoppa_without_deps.yml',
        )
        ConfigParser().parse('')['dependencies'].should.be.equal([])

    def test_parse_with_errors(self):
        """Test parsse with errors"""
        ConfigParser._get_config_path.return_value = os.path.join(
            FIXTURES_PATH, 'pytoppa_with_errors.yml',
        )
        ConfigParser().parse.when.called_with('').should.throw(ParsingError)
