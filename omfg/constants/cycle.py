"""
Wrapper around datetime to make working with rose/cylc style date strings simpler.
"""

from datetime import datetime as dt, timedelta


class Cycle:
    """Simple wrapper around datetime"""
    def __init__(self, cylc_string):
        self._cylc_string = cylc_string
        self._datetime = dt.strptime(cylc_string, "%Y%m%dT%H%MZ")

    def __str__(self):
        return self._cylc_string

    def __eq__(self, other):
        if isinstance(other, Cycle):
            return self.datetime == other.datetime
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Cycle):
            return self.datetime > other.datetime
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Cycle):
            return self.datetime < other.datetime
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Cycle):
            return self.datetime >= other.datetime
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Cycle):
            return self.datetime <= other.datetime
        return NotImplemented

    @property
    def datetime(self):
        """The underlying datetime object"""
        return self._datetime

    def increment(self):
        """Add six hours"""
        self._datetime += timedelta(hours=6)

    def decrement(self):
        """Subtract six hours"""
        self._datetime -= timedelta(hours=6)
