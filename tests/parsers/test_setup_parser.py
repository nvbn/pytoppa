import os
import pytest
from pytoppa.parsers.setup_parser import SetupParser
from pytoppa.parsers.exceptions import ParsingError


def test_parse_setup_py(fixtures_path):
    """Test parse setup.py"""
    result = SetupParser().parse(fixtures_path)
    assert result['author'] == 'Vladimir Iakovlev'


def test_stup_py_not_found(fixtures_path):
    """Test setup.py not found"""
    path = os.path.join(fixtures_path, '..')
    with pytest.raises(ParsingError):
        SetupParser().parse(path)
