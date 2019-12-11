"""Tests for column"""
import pytest
from ...context import omfg


@pytest.fixture(name="column")
def column_fixture():
    """Fixture for reusable Column object"""
    return omfg.constants.Column.get_column("corvalue@body")


def test_str(column):
    """Test the __str__ method"""
    assert str(column) == "corvalue"


def test_name(column):
    """Test the name method"""
    assert column.name == "corvalue@body"


def test_label(column):
    """Test the label method"""
    assert column.label == "Corrected"


def test_is_depar(column):
    """Test the is_depar method"""
    assert omfg.constants.Column.get_column("an_depar@body").is_depar
    assert not column.is_depar


def test_get_column_invalid_name():
    """Test the get column method with an invalid name"""
    with pytest.raises(ValueError):
        omfg.constants.Column.get_column("foo")
