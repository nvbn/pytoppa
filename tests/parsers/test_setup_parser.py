import sure
from unittest import TestCase
from pytoppa.parsers.setup_parser import SetupParser
from ..base import FIXTURES_PATH


class SetupParserCase(TestCase):
    """Case for setup.py parser"""

    def test_parse_setup_py(self):
        """Test parse setup.py"""
        result = SetupParser().parse(FIXTURES_PATH)
        result['author'].should.be.equal('Vladimir Iakovlev')
