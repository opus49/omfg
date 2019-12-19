"""Tests for loginit"""
import logging
from ...context import omfg


def test_loginit(monkeypatch):
    """Test the loginit function"""
    global basic_config
    basic_config = None

    def mock_basicConfig(*args, **kwargs):
        global basic_config
        basic_config = kwargs
    monkeypatch.setattr(logging, "basicConfig", mock_basicConfig)
    assert basic_config is None
    omfg.util.loginit("foo")
    assert basic_config["level"] == "foo"
