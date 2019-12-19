"""Tests for StopWatch"""
import pytest
import time
from ...context import omfg


@pytest.fixture(name="stopwatch")
def stopwatch_fixture(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 0)
    return omfg.util.StopWatch()


def test_first(stopwatch):
    """Test the first method"""
    assert stopwatch.first == 0


def test_last(monkeypatch, stopwatch):
    """Test the last method"""
    monkeypatch.setattr(time, "time", lambda: 1)
    assert stopwatch.last == 0
    stopwatch.mark()
    assert stopwatch.previous == 0
    stopwatch.mark()
    assert stopwatch.previous == 1


def test_previous(monkeypatch, stopwatch):
    """Test the previous method"""
    monkeypatch.setattr(time, "time", lambda: 1)
    assert stopwatch.previous == 0
    stopwatch.mark()
    assert stopwatch.last == 1


def test_get_total_elapsed_zero_zero(monkeypatch, stopwatch):
    """Test the total_elapsed method with zero hours, zero minutes"""
    monkeypatch.setattr(time, "time", lambda: 5.0345)
    stopwatch.mark()
    assert stopwatch.get_total_elapsed() == "0 minutes, 5.03 seconds"


def test_get_total_elapsed_zero_one(monkeypatch, stopwatch):
    """Test the total_elapsed method with zero hours, one minute"""
    monkeypatch.setattr(time, "time", lambda: 67.9675)
    stopwatch.mark()
    assert stopwatch.get_total_elapsed() == "1 minute, 7.97 seconds"


def test_get_total_elapsed_one_two(monkeypatch, stopwatch):
    """Test the total_elapsed method with one hour, two minutes"""
    monkeypatch.setattr(time, "time", lambda: 3720.0)
    stopwatch.mark()
    assert stopwatch.get_total_elapsed() == "1 hour, 2 minutes, 0.00 seconds"


def test_get_total_elapsed_two_two(monkeypatch, stopwatch):
    """Test the total_elapsed method with two hour, two minutes"""
    monkeypatch.setattr(time, "time", lambda: 7320.0)
    stopwatch.mark()
    assert stopwatch.get_total_elapsed() == "2 hours, 2 minutes, 0.00 seconds"
