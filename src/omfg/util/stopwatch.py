"""Module for keeping track of execution times"""

import time


class StopWatch:
    """
    Just a simple object to keep track of time elapsed during execution.
    When the object is created, the stopwatch begins.  Any calls to mark
    will add additional entries.

    Example usage:
    >>> watch = StopWatch()
    >>> watch.mark()
    >>> watch.mark()
    >>> print(f"Task elapsed time: {watch.last - watch.previous}")
    >>> watch.mark()
    >>> print(f"Total elapsed time: {watch.get_total_elapsed()}")
    """
    def __init__(self):
        self._times = [time.time()]

    @property
    def first(self):
        """Get the first time on the stopwatch"""
        return self._times[0]

    @property
    def last(self):
        """Get the last time on the stopwatch"""
        return self._times[-1]

    def mark(self):
        """Mark the stopwatch with the current time"""
        self._times.append(time.time())

    @property
    def previous(self):
        """Get the time before the most recent mark"""
        if len(self._times) < 2:
            return self._times[-1]
        return self._times[-2]

    def get_total_elapsed(self):
        """Get a formatted string representing the total elapsed time on the stopwatch"""
        return self._format(self.last - self.first)

    @staticmethod
    def _format(elapsed_seconds):
        """A quick formatter for human-readable timestamp."""
        hours, seconds = divmod(elapsed_seconds, 3600.0)
        minutes, seconds = divmod(seconds, 60.0)
        hours = int(hours)
        minutes = int(minutes)
        result = f"{minutes} minute{'s' if minutes != 1 else ''}, {seconds:.2f} seconds"
        if hours > 0:
            result = f"{hours} hour{'s' if hours != 1 else ''}, {result}"
        return result
