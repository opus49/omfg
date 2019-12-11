"""Tests for column"""
import pytest
from ...context import omfg


def test_from_type_invalid():
    """Test from_type method with an invalid varno type"""
    with pytest.raises(ValueError):
        omfg.constants.VarnoType.from_type("foo")
