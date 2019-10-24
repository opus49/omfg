"""Plan View for generating map based charts"""

from pathlib import Path
from .chart import Chart
import cartopy


class Planview(Chart):
    """Map-based chart"""
    cartopy.config["data_dir"] = str(Path(__file__) / "cartopy")
