"""Tests for loginit"""
from datetime import datetime as dt
import logging
import os
import pytest
from unittest.mock import patch
from ..context import omfg


class MockApp(omfg.BaseApp):
    """
    For this mock app, pos_args and opt_args should be
    dictionaries where the key is the long argument name
    and the value is the user-supplied value.  These will
    be used by the get_arg method to simulate command-line
    arguments.
    """
    @staticmethod
    def _parse(pos_args, opt_args):
        """Override the argument parsing"""
        pos_args = {} if not pos_args else pos_args
        opt_args = {} if not opt_args else opt_args
        return {**pos_args, **opt_args}

    def _run(self):
        raise NotImplementedError()


@pytest.fixture(name="mock_app")
def mock_app_fixture():
    return MockApp()


def mock_true(*args, **kwargs):
    return True


def mock_false(*args, **kwargs):
    return False


def test_get_log_level(mock_app):
    assert mock_app._get_log_level() == omfg.DEFAULT_LOG_LEVEL


def test_get_log_level_handles_user_input():
    app = MockApp(opt_args={"loglevel": "WARNING"})
    assert app._get_log_level() == logging.WARNING


def test_get_log_level_handles_invalid_user_input():
    app = MockApp(opt_args={"loglevel": "foo"})
    assert app._get_log_level() == omfg.DEFAULT_LOG_LEVEL


def test_get_arg():
    app = MockApp(pos_args={"file": "/foo.txt"}, opt_args={"verbose": True})
    assert app.get_arg("file") == "/foo.txt"
    assert app.get_arg("verbose")
    assert app.get_arg("foo") is None


def test_get_hostname(mock_app, monkeypatch):
    monkeypatch.setattr(omfg.app.socket, "gethostname", lambda: "foo")
    assert mock_app.get_hostname() == "foo"


def test_get_timestamp(mock_app):
    with patch("omfg.app.dt") as mock_dt:
        mock_dt.now.return_value = dt(2020, 1, 1, 12, 34, 56)
        assert mock_app.get_timestamp() == "2020-01-01T12:34:56Z"


def test_validate_directory_valid(mock_app, monkeypatch):
    monkeypatch.setattr(os.path, "isdir", mock_true)
    try:
        mock_app.validate_directory("foo")
    except OSError:
        pytest.fail("Unexpected OSError")


def test_validate_directory_invalid(mock_app, monkeypatch):
    monkeypatch.setattr(os.path, "isdir", mock_false)
    with pytest.raises(OSError):
        mock_app.validate_directory("foo")
