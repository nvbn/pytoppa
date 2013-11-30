import sure
import os
from unittest import TestCase
from pytoppa.parsers.setup_parser import SetupParser
from pytoppa.parsers.exceptions import ParsingError
from ..base import FIXTURES_PATH


class SetupParserCase(TestCase):
    """Case for setup.py parser"""

    def test_parse_setup_py(self):
        """Test parse setup.py"""
        result = SetupParser().parse(FIXTURES_PATH)
        result['author'].should.be.equal('Vladimir Iakovlev')

    def test_stup_py_not_found(self):
        """Test setup.py not found"""
        path = os.path.join(FIXTURES_PATH, '..')
        SetupParser().parse.when.called_with(path)\
            .should.throw(ParsingError)
