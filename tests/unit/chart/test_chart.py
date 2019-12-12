"""Unit tests for chart class"""

import pytest
from ...context import omfg


@pytest.fixture(name="config")
def config_fixture():
    """Fixture for a generic config"""
    return omfg.chart.Config(
        cache=0,
        chart_type=None,
        column="",
        cycle1="20190830T0000Z",
        cycle2="20190830T1200Z",
        data_path="/data",
        obs_group=None,
        varno_code=39,
        vertco_max=1.0,
        vertco_min=2.0,
        vertco_type_code=7
    )


@pytest.fixture(name="chart")
def chart_fixture(monkeypatch, config):
    """Fixture for a generic abstract chart"""
    monkeypatch.setattr(omfg.chart.chart.Chart, "__abstractmethods__", set())
    return omfg.chart.chart.Chart(config)


def test_generate(monkeypatch, chart):
    global generated
    generated = 0

    def generate(*args, **kwargs):
        global generated
        generated += 1

    def mkdir(*args, **kwargs):
        pass

    monkeypatch.setattr(omfg.chart.chart.Path, "mkdir", mkdir)
    monkeypatch.setattr(omfg.chart.chart.Chart, "_generate", generate)
    assert not generated
    chart.generate()
    assert generated


def test_generate_with_cache(monkeypatch, chart):
    global generated
    generated = 0

    def generate(*args, **kwargs):
        global generated
        generated += 1

    def mkdir(*args, **kwargs):
        pass

    def is_file(*args, **kwargs):
        return True

    chart.config._cache = 1
    monkeypatch.setattr(omfg.chart.chart.Path, "mkdir", mkdir)
    monkeypatch.setattr(omfg.chart.chart.Path, "is_file", is_file)
    monkeypatch.setattr(omfg.chart.chart.Chart, "_generate", generate)
    assert not generated
    chart.generate()
    assert not generated
