import os
import pytest


@pytest.fixture
def fixtures_path():
    return os.path.join(os.path.dirname(__file__), 'fixtures')
