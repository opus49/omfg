"""Module for generating charts"""

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Chart(ABC):
    """Abstract class for charts"""
    def __init__(self, config):
        self.config = config
        self.figure = plt.figure

    @abstractmethod
    def generate(self):
        """Generate the chart and return the absolute path to the png file."""
