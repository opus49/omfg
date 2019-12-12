"""Used to share fixtures among tests"""
import pytest
from .context import omfg


@pytest.fixture(name="timeseries_config")
def timeseries_config_fixture():
    """Fixture for a timeseries config"""
    return omfg.chart.Config(
        cache=0,
        chart_type="timeseries",
        column="",
        cycle1="20190830T0000Z",
        cycle2="20190830T1200Z",
        data_path="/data",
        obs_group=None,
        varno_code=39,
        vertco_max=2.0,
        vertco_min=1.0,
        vertco_type_code=7
    )


@pytest.fixture(name="planview_config")
def planview_config_fixture():
    """Fixture for a planview config"""
    return omfg.chart.Config(
        cache=0,
        chart_type="planview",
        column="an_depar@body",
        cycle1="20190830T0000Z",
        cycle2="20190830T0000Z",
        data_path="/data",
        obs_group=None,
        varno_code=39,
        vertco_max=2.0,
        vertco_min=1.0,
        vertco_type_code=7
    )
