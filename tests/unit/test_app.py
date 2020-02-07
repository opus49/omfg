"""Tests for loginit"""
import argparse
from datetime import datetime as dt
import logging
import os
import pathlib
import pytest
# import shutil
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


class MockAppNoParse(omfg.BaseApp):
    def _run(self):
        raise NotImplementedError()


class MockArgumentParser:
    def __init__(self):
        self.args = []

    def add_argument(self, *args, **kwargs):
        args_string = ",".join(args)
        kwargs_string = ",".join([f"{x}={y}" for x, y in kwargs.items()])
        self.args.append(",".join([args_string, kwargs_string]))

    def parse_args(self):
        return argparse.Namespace(args=self.args)


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


def test_parse(monkeypatch):
    monkeypatch.setattr(argparse, "ArgumentParser", MockArgumentParser)
    app = MockAppNoParse(
        pos_args=(["filename", "The filename", str],),
        opt_args=(
            ["m", "max", "Maximum", int],
            ["v", "verbose", "Do it verbosely", bool]
        )

    )
    assert len(app._args["args"]) == 3
    assert app._args["args"][0] == "filename,help=The filename,type=<class 'str'>"
    assert app._args["args"][1] == "-m,--max,dest=max,help=Maximum,type=<class 'int'>"
    assert app._args["args"][2] == "-v,--verbose,dest=verbose,help=Do it verbosely" \
        ",action=store_true,default=False"


def test_parse_pos_only(monkeypatch):
    monkeypatch.setattr(argparse, "ArgumentParser", MockArgumentParser)
    app = MockAppNoParse(
        pos_args=(["filename", "The filename", str],)
    )
    assert len(app._args["args"]) == 1
    assert app._args["args"][0] == "filename,help=The filename,type=<class 'str'>"


def test_parse_opt_only(monkeypatch):
    monkeypatch.setattr(argparse, "ArgumentParser", MockArgumentParser)
    app = MockAppNoParse(
        opt_args=(
            ["m", "max", "Maximum", int],
            ["v", "verbose", "Do it verbosely", bool]
        )

    )
    assert len(app._args["args"]) == 2
    assert app._args["args"][0] == "-m,--max,dest=max,help=Maximum,type=<class 'int'>"
    assert app._args["args"][1] == "-v,--verbose,dest=verbose,help=Do it verbosely" \
        ",action=store_true,default=False"


def test_prepare_directory_already_a_file(mock_app, monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", mock_true)
    with pytest.raises(OSError):
        mock_app.prepare_directory("foo")


def test_prepare_directory_preserve(mock_app, monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", mock_false)
    monkeypatch.setattr(pathlib.Path, "is_dir", mock_true)
    with patch("shutil.rmtree") as mock_rmtree:
        with patch.object(pathlib.Path, "mkdir") as mock_mkdir:
            mock_app.prepare_directory("foo")
            mock_rmtree.assert_not_called()
            mock_mkdir.assert_called_with(exist_ok=True)


def test_prepare_directory_destroy(mock_app, monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", mock_false)
    monkeypatch.setattr(pathlib.Path, "is_dir", mock_true)
    with patch("shutil.rmtree") as mock_rmtree:
        with patch.object(pathlib.Path, "mkdir") as mock_mkdir:
            mock_app.prepare_directory("foo", True)
            mock_rmtree.assert_called_with("foo")
            mock_mkdir.assert_called_with(exist_ok=True)


def test_prepare_directory_destroy_rmtree_fails(mock_app, monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", mock_false)
    monkeypatch.setattr(pathlib.Path, "is_dir", mock_true)
    with patch("shutil.rmtree") as mock_rmtree:
        with patch.object(pathlib.Path, "mkdir") as mock_mkdir:
            mock_rmtree.side_effect = OSError()
            with pytest.raises(OSError):
                mock_app.prepare_directory("foo", True)
                mock_rmtree.assert_called_with("foo")
                mock_mkdir.assert_called_with(exist_ok=True)


def test_prepare_directory_destroy_mkdir_fails(mock_app, monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", mock_false)
    monkeypatch.setattr(pathlib.Path, "is_dir", mock_true)
    with patch("shutil.rmtree") as mock_rmtree:
        with patch.object(pathlib.Path, "mkdir") as mock_mkdir:
            mock_mkdir.side_effect = OSError()
            with pytest.raises(OSError):
                mock_app.prepare_directory("foo", True)
                mock_rmtree.assert_called_with("foo")
                mock_mkdir.assert_called_with(exist_ok=True)
