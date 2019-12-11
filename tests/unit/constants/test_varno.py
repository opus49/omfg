"""Tests for varno"""
import pytest
from ...context import omfg


@pytest.fixture(name="temperature_type_lookup")
def temperature_type_lookup_fixture():
    """Fixture for looking up temperature varno type from the VARNO_TYPES table"""
    return omfg.constants.VARNO_TYPES["temperature"]


@pytest.fixture(name="t2m_lookup")
def t2m_lookup_fixture():
    """Fixture for looking up t2m from VARNO_TABLE"""
    return omfg.constants.VARNO_TABLE["t2m"]


@pytest.fixture(name="t2m")
def t2m_fixture(t2m_lookup):
    """Fixture for reusable Varno object"""
    return omfg.constants.Varno.get_varno(t2m_lookup["code"])


def test_str(t2m, t2m_lookup):
    """Test the __str__ method"""
    assert str(t2m) == str(t2m_lookup["code"])


def test_name(t2m, t2m_lookup):
    """Test the name method"""
    assert t2m.name == "t2m"


def test_code(t2m):
    """Test the code method"""
    assert omfg.constants.Varno.get_varno(39).code == 39


def test_desc(t2m, t2m_lookup):
    """Test the desc method"""
    assert t2m.desc == t2m_lookup["desc"]


def test_cmap(t2m, temperature_type_lookup):
    """Test the cmap method"""
    assert t2m.cmap == temperature_type_lookup["cmap"]


def test_formula(t2m, temperature_type_lookup):
    """Test the formula method"""
    assert t2m.formula == temperature_type_lookup["formula"]


def test_levels(t2m, temperature_type_lookup):
    """Test the levels method"""
    assert t2m.levels == temperature_type_lookup["levels"]


def test_units(t2m, temperature_type_lookup):
    """Test the units method"""
    assert t2m.units == temperature_type_lookup["units"]


def test_get_varno_not_in_table():
    """Test the get_varno method with an invalid code"""
    with pytest.raises(ValueError):
        omfg.constants.Varno.get_varno(-1)


def test_get_varno_without_type():
    """Test the get_varno method with a varno that doesn't have a type"""
    test_varno = omfg.constants.Varno.get_varno(215)
    assert test_varno.cmap is None
    assert test_varno.formula is None
    assert test_varno.levels is None
    assert test_varno.units is None


def test_get_name_invalid_code():
    """Test the get_name method with an invalid code"""
    assert omfg.constants.Varno.get_name(-1) == omfg.constants.UNKNOWN
    assert omfg.constants.Varno.get_name("foo") == omfg.constants.UNKNOWN


def test_get_type_valid(temperature_type_lookup):
    """Test the get type method when there is a type"""
    test_type = omfg.constants.Varno.get_type("t2m")
    assert test_type.cmap == temperature_type_lookup["cmap"]
    assert test_type.formula == temperature_type_lookup["formula"]
    assert test_type.levels == temperature_type_lookup["levels"]
    assert test_type.units == temperature_type_lookup["units"]


def test_get_type_no_type():
    """Test the get type method when there is no type"""
    test_type = omfg.constants.Varno.get_type("1dvar")
    assert test_type.cmap is None
    assert test_type.formula is None
    assert test_type.levels is None
    assert test_type.units is None


def test_get_type_invalid_name():
    """Test the get type method when the name is invalid"""
    test_type = omfg.constants.Varno.get_type("foo")
    assert test_type.cmap is None
    assert test_type.formula is None
    assert test_type.levels is None
    assert test_type.units is None


def test_get_code(t2m_lookup):
    """Test the get code method"""
    assert omfg.constants.Varno.get_code("t2m") == t2m_lookup["code"]


def test_get_code_invalid_name():
    """Test the get code method with an invalid name"""
    assert omfg.constants.Varno.get_code("foo") == omfg.constants.UNKNOWN


def test_get_desc(t2m_lookup):
    """Test the get desc method"""
    assert omfg.constants.Varno.get_desc("t2m") == t2m_lookup["desc"]


def test_get_desc_invalid_name():
    """Test the get desc method with an invalid name"""
    assert omfg.constants.Varno.get_desc("foo") == omfg.constants.UNKNOWN
