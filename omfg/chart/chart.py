"""Module for generating charts"""

from abc import ABC, abstractmethod
from pathlib import Path
import matplotlib.pyplot as plt


class Chart(ABC):
    """Abstract class for charts"""
    def __init__(self, config):
        self.config = config
        self.figure = plt.figure(figsize=(12, 8))

    @abstractmethod
    def generate(self):
        """Generate the chart and return the absolute path to the png file."""

    @staticmethod
    def get_omfg_path():
        """Get the Path to the user's omfg directory"""
        omfg_path = Path.home() / ".omfg"
        omfg_path.mkdir(exist_ok=True)
        return omfg_path
