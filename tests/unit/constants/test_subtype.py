"""Tests for subtype"""
from ...context import omfg


def test_get_name():
    """Test the get_name method"""
    assert omfg.constants.Subtype.get_name(20400) == "aatsr"
    assert omfg.constants.Subtype.get_name(22300) == "esacswvw"
    assert omfg.constants.Subtype.get_name(-1) is None


def test_get_code():
    """Test the get_code method"""
    assert omfg.constants.Subtype.get_code("buoy") == 11700
    assert omfg.constants.Subtype.get_code("gpsro") == 22900
    assert omfg.constants.Subtype.get_code("foobar") is None
