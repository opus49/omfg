"""Unit tests for chart class"""

import pytest
from ...context import omfg


@pytest.fixture(name="chart")
def chart_fixture(monkeypatch, planview_config):
    """Fixture for a generic abstract chart"""
    monkeypatch.setattr(omfg.chart.chart.Chart, "__abstractmethods__", set())
    return omfg.chart.chart.Chart(planview_config)


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
