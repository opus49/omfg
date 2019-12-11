"""Tests for column"""
import pytest
from ...context import omfg


@pytest.fixture(name="vertco_type")
def vertco_type_fixture():
    """Fixture for resuable VertcoType object"""
    return omfg.constants.VertcoType.get_vertco_type(1)


def test_str(vertco_type):
    """Test for __str__ method"""
    assert str(vertco_type) == "1"


def test_code(vertco_type):
    """Test for code method"""
    assert vertco_type.code == 1


def test_label(vertco_type):
    """Test for label method"""
    assert vertco_type.label == "Pressure"


def test_get_vertco_type_unknown_code():
    """Test get_vertco_type method with an unknown code"""
    with pytest.raises(ValueError):
        omfg.constants.VertcoType.get_vertco_type(-1)


def test_get_vertco_type_invalid_code():
    """Test get_vertco_type method with an invalid code"""
    with pytest.raises(ValueError):
        omfg.constants.VertcoType.get_vertco_type("foo")
