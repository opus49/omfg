"""Module for generating charts"""

from abc import ABC, abstractmethod
from pathlib import Path
import matplotlib as mpl
# pylint: disable=wrong-import-position,wrong-import-order
mpl.use("AGG")
import matplotlib.pyplot as plt


class Chart(ABC):
    """Abstract class for charts"""
    def __init__(self, config):
        mpl.rcParams["font.sans-serif"] = "Noto Mono"
        mpl.rcParams["font.family"] = "sans-serif"
        self.config = config
        self.figure = plt.figure(figsize=(12, 8))

    def generate(self):
        """Generate the chart and return the absolute path to the png file."""
        if self.config.use_cache:
            if self.output_filepath.is_file():
                return str(self.output_filepath)
        self._generate()
        return str(self.output_filepath)

    @abstractmethod
    def _generate(self):
        """Subclasses should implement this method for the chart generation logic"""

    @staticmethod
    def get_omfg_path():
        """Get the Path to the user's omfg directory"""
        omfg_path = Path.home() / ".omfg"
        omfg_path.mkdir(exist_ok=True)
        return omfg_path

    @property
    def output_filepath(self):
        """Get the output Path object to use for generating images"""
        return self.get_omfg_path() / f"{self.config.get_output_filestem()}.png"