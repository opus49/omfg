"""Module for generating charts"""

from abc import ABC, abstractmethod
import pathlib
import matplotlib.pyplot as plt


class Chart:
    """Abstract class for charts"""
    def __init__(self):
        self.figure = plt.figure
