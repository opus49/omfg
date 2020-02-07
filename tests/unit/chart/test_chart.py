"""Unit tests for chart class"""

import pytest
from ...context import chart


class MockChart(chart.chart.Chart):
    def __init__(self, config):
        super().__init__(config)
        self.generated = False

    def _generate(self):
        self.generated = True


def mock_true(*args, **kwargs):
    return True


def mock_false(*args, **kwargs):
    return False


@pytest.fixture(name="planview_chart")
def planview_chart_fixture(planview_config):
    """Fixture for a generic abstract chart with planview config"""
    return MockChart(planview_config)


@pytest.fixture(name="planview_chart_with_cache")
def planview_chart_with_cache_fixture(monkeypatch, planview_config):
    """Fixture for a generic abstract chart with planview config and cache"""
    monkeypatch.setattr(planview_config, "_cache", 1)
    return MockChart(planview_config)


@pytest.fixture(name="planview_chart_with_same_vertco")
def planview_chart_with_same_vertco_fixture(monkeypatch, planview_config):
    """Fixture for a generic abstract chart with planview config and matching min/max vertco"""
    monkeypatch.setattr(planview_config, "_vertco_max", 3.0)
    monkeypatch.setattr(planview_config, "_vertco_min", 3.0)
    return MockChart(planview_config)


def test_generate_without_cache(planview_chart):
    assert not planview_chart.generated
    planview_chart.generate()
    assert planview_chart.generated


def test_generate_with_cache(monkeypatch, planview_chart_with_cache):
    assert not planview_chart_with_cache.generated
    monkeypatch.setattr(chart.chart.Path, "is_file", mock_true)
    planview_chart_with_cache.generate()
    assert not planview_chart_with_cache.generated
    monkeypatch.setattr(chart.chart.Path, "is_file", mock_false)
    planview_chart_with_cache.generate()
    assert planview_chart_with_cache.generated


def test_get_vertco_label(planview_chart):
    assert planview_chart.get_vertco_label() == "Channel Number: 1 - 2"


def test_get_vertco_label_same_vertco(planview_chart_with_same_vertco):
    assert planview_chart_with_same_vertco.get_vertco_label() == "Channel Number: 3"
