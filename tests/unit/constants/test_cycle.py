"""Tests for cycle"""
from datetime import datetime as dt
import pytest
from ...context import omfg


@pytest.fixture(name="cycle")
def cycle_fixture():
    """Fixture for resuable Cycle object"""
    return omfg.constants.Cycle("20190830T1200Z")


def test_str(cycle):
    """Test for __str__ method"""
    assert str(cycle) == "20190830T1200Z"


def test_eq(cycle):
    """Test for __eq__ method"""
    assert cycle == omfg.constants.Cycle("20190830T1200Z")
    assert cycle != omfg.constants.Cycle("20190830T0000Z")


def test_eq_not_implemented(cycle):
    """Test for __eq__ method with non Cycle object"""
    assert cycle != "foo"
    assert cycle != 1


def test_gt(cycle):
    """Test for __gt__ method"""
    assert cycle > omfg.constants.Cycle("20190830T0000Z")


def test_gt_not_implemented(cycle):
    """Test the __gt__ method with a non Cycle object"""
    with pytest.raises(TypeError):
        assert cycle > "foo"
    with pytest.raises(TypeError):
        assert cycle > 1


def test_lt(cycle):
    """Test for __lt__ method"""
    assert cycle < omfg.constants.Cycle("20190901T0000Z")


def test_lt_not_implemented(cycle):
    """Test the __lt__ method with a non Cycle object"""
    with pytest.raises(TypeError):
        assert cycle < "foo"
    with pytest.raises(TypeError):
        assert cycle < 1


def test_ge(cycle):
    """Test for __ge__ method"""
    assert cycle >= omfg.constants.Cycle("20190830T0000Z")
    assert cycle >= omfg.constants.Cycle("20190830T1200Z")


def test_ge_not_implemented(cycle):
    """Test the __ge__ method with a non Cycle object"""
    with pytest.raises(TypeError):
        assert cycle >= "foo"
    with pytest.raises(TypeError):
        assert cycle >= 1


def test_le(cycle):
    """Test for __le__ method"""
    assert cycle <= omfg.constants.Cycle("20190830T1200Z")
    assert cycle <= omfg.constants.Cycle("20190830T1800Z")


def test_le_not_implemented(cycle):
    """Test the __le__ method with a non Cycle object"""
    with pytest.raises(TypeError):
        assert cycle <= "foo"
    with pytest.raises(TypeError):
        assert cycle <= 1


def test_datetime(cycle):
    """Test for datetime method"""
    assert cycle.datetime == dt.strptime("201908301200", "%Y%m%d%H%M")


def test_increment(cycle):
    """Test increment method"""
    cycle.increment()
    assert str(cycle) == "20190830T1800Z"


def test_decrement(cycle):
    """Test decrement method"""
    cycle.decrement()
    assert str(cycle) == "20190830T0600Z"
