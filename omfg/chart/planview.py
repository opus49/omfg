"""Plan View for generating map based charts"""

from pathlib import Path
import cartopy
from .chart import Chart


class Planview(Chart):
    """Map-based chart"""
    cartopy.config["data_dir"] = str(Path(__file__) / "cartopy")

    def generate(self):
        """Generate the chart"""
        pass
