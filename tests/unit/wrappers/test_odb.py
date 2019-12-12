"""Tests for odb"""
import pytest
from ...context import omfg


MOCK_DATA = (
    [0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 1, 1, 1.0, 1.0, 1],
    [0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 1, 2, 1.0, 1.0, 1],
    [1.0, 1.0, 1, 0.0, 0.0, 0.0, 0.0, 1, 2, 1.0, 1.0, 1],
)


class MockReader:
    def __init__(self, filename, sql_command):
        self._index = -1
        varno = self._get_varno(sql_command)
        self._data = self._get_varno_data(varno)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self._data):
            raise StopIteration
        return self._data[self._index]

    @staticmethod
    def _get_varno(sql_command):
        if "WHERE varno" not in sql_command:
            return None
        _, varno = sql_command.split("=")
        return int(varno)

    @staticmethod
    def _get_varno_data(varno):
        if varno is None:
            return MOCK_DATA
        data = []
        for entry in MOCK_DATA:
            if int(entry[8]) == int(varno):
                data.append(entry)
        return tuple(data)


@pytest.fixture(name="odb_default")
def odb_default_fixture(monkeypatch):
    """Fixture for generating an ODB object using default fields"""
    def mock_reader(*args, **kwargs):
        return MockReader(args[0], args[1])

    monkeypatch.setattr(omfg.wrappers.odb, "Reader", mock_reader)
    return omfg.wrappers.ODB("test")


@pytest.fixture(name="odb_varno2")
def odb_varno2_fixture(monkeypatch):
    """Fixture for generating an ODB object using varno 2"""
    def mock_reader(*args, **kwargs):
        return MockReader(args[0], args[1])

    monkeypatch.setattr(omfg.wrappers.odb, "Reader", mock_reader)
    return omfg.wrappers.ODB("test", varno=2)


def test_varnos(odb_default, odb_varno2):
    """Test for the varnos method"""
    assert len(odb_default.varnos) == 2
    assert 1 in odb_default.varnos
    assert 2 in odb_default.varnos
    assert len(odb_varno2.varnos) == 1
    assert 1 not in odb_varno2.varnos
    assert 2 in odb_varno2.varnos


def test_get_varno_data(odb_default, odb_varno2):
    """Test for the get_varno_data method"""
    assert len(odb_default.get_varno_data(0)) == 0
    assert len(odb_default.get_varno_data(1)) == 1
    assert len(odb_default.get_varno_data(2)) == 2
    assert len(odb_varno2.get_varno_data(1)) == 0
    assert len(odb_varno2.get_varno_data(2)) == 2
