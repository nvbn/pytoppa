import os
import pytest
from unittest.mock import MagicMock
from pytoppa.parsers.config_parser import ConfigParser
from pytoppa.parsers.exceptions import ParsingError


@pytest.fixture(autouse=True)
def config_path(request):
    """Mock _get_config_path method"""
    orig_config_path = ConfigParser._get_config_path

    def restore_config_path():
        ConfigParser._get_config_path = orig_config_path

    request.addfinalizer(restore_config_path)
    ConfigParser._get_config_path = MagicMock()
    return ConfigParser._get_config_path


def test_parse_config(config_path, fixtures_path):
    """Test parse config"""
    config_path.return_value = os.path.join(fixtures_path, 'pytoppa.yml')
    assert ConfigParser().parse('')['section'] == 'net'


def test_parse_without_section(config_path, fixtures_path):
    """Test parse without section"""
    config_path.return_value = os.path.join(
        fixtures_path, 'pytoppa_without_section.yml')
    assert ConfigParser().parse('')['section'] == 'python'


def test_parse_without_deps(config_path, fixtures_path):
    """Test parse without deps"""
    config_path.return_value = os.path.join(
        fixtures_path, 'pytoppa_without_deps.yml')
    assert ConfigParser().parse('')['dependencies'] == []


def test_parse_with_errors(config_path, fixtures_path):
    """Test parse with errors"""
    config_path.return_value = os.path.join(
        fixtures_path, 'pytoppa_with_errors.yml')
    with pytest.raises(ParsingError):
        ConfigParser().parse('')
