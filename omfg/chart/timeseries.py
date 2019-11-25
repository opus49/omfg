"""Time series for generating map based charts"""

from .chart import Chart


class Timeseries(Chart):
    """Time-series based chart"""

    def _generate(self):
        """Generate the chart"""
