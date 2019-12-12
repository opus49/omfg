"""Unit tests for Chart Config"""
from unittest.mock import patch
from ...context import omfg


MOCK_CONFIG_DATA = {
    "cache": "0",
    "chart_type": "planview",
    "column": "an_depar@body",
    "obs_group": "surface",
    "vertco_max": "1",
    "varno_code": "39",
    "vertco_type_code": 5,
    "cycle2": "20191029T1000Z",
    "vertco_min": "1",
    "cycle1": "20191027T0000Z",
    "data_path": "/home/puskarm/data/valid"
}


def test_use_cache(timeseries_config):
    """Test the use_cache method"""
    assert not timeseries_config.use_cache


def test_chart_type(timeseries_config):
    """Test the chart_type method"""
    assert timeseries_config.chart_type == "timeseries"


def test_column(timeseries_config):
    """Test the column method"""
    assert timeseries_config.column is None


def test_cycle1(timeseries_config):
    """Test the cycle1 method"""
    assert str(timeseries_config.cycle1) == "20190830T0000Z"


def test_cycle2(timeseries_config):
    """Test the cycle2 method"""
    assert str(timeseries_config.cycle2) == "20190830T1200Z"


def test_data_path(timeseries_config):
    """Test the data_path method"""
    assert timeseries_config.data_path.name == "data"


def test_obs_group(timeseries_config):
    """Test the obs_group method"""
    assert timeseries_config.obs_group is None


def test_varno(timeseries_config):
    """Test the varno method"""
    assert timeseries_config.varno.name == "t2m"


def test_vertco_max(timeseries_config):
    """Test the vertco_max method"""
    assert int(timeseries_config.vertco_max) == 2


def test_vertco_min(timeseries_config):
    """Test the vertco_min method"""
    assert int(timeseries_config.vertco_min) == 1


def test_vertco_type(timeseries_config):
    """Test the vertco_type method"""
    assert timeseries_config.vertco_type.label == "Channel Number"


def test_is_depar_false(timeseries_config):
    """Test the is_depar method with false result"""
    assert not timeseries_config.is_depar


def test_is_depar_true(planview_config):
    """Test the is_depar method with true result"""
    assert planview_config.is_depar


def test_get_output_filestem(timeseries_config, planview_config):
    """Test the get_output_filestem method"""
    assert timeseries_config.get_output_filestem() == \
        "timeseries_39_7_20190830T0000Z_20190830T1200Z_1.0_2.0"
    assert planview_config.get_output_filestem() == \
        "planview_an_depar_39_7_20190830T0000Z_20190830T0000Z_1.0_2.0"


def test_load():
    """Test for the load method"""
    with patch("builtins.open"):
        with patch("omfg.chart.config.json.load", return_value=MOCK_CONFIG_DATA):
            config = omfg.chart.Config.load("foo")
            assert not config.use_cache
            assert config.chart_type == "planview"
            assert config.obs_group == "surface"
            assert config.varno.code == "39"
            assert config.is_depar
