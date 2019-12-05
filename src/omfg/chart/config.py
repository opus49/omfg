"""Explicit definition of user configuration options for chart generators"""

import json
from pathlib import Path
import numpy as np
from omfg.constants import Column, Cycle, Varno, VertcoType


_FILESTEM_PROPERTIES = [
    "chart_type",
    "column",
    "obs_group",
    "varno",
    "vertco_type",
    "cycle1",
    "cycle2",
    "vertco_min",
    "vertco_max"
]


class Config:
    """Explicit object.  Expects strings parsed from JSON file as parameters"""
    #pylint: disable=too-many-instance-attributes,too-many-arguments
    def __init__(self, cache, chart_type, column, cycle1, cycle2, data_path,
                 obs_group, varno_code, vertco_max, vertco_min, vertco_type_code):
        self._cache = int(cache)
        self._chart_type = chart_type
        self._column = Column.get_column(column) if column else None
        self._cycle1 = Cycle(cycle1)
        self._cycle2 = Cycle(cycle2)
        self._data_path = Path(data_path)
        self._obs_group = obs_group
        self._varno = Varno.get_varno(varno_code)
        self._vertco_max = np.float(vertco_max)
        self._vertco_min = np.float(vertco_min)
        self._vertco_type = VertcoType.get_vertco_type(vertco_type_code)

    @property
    def use_cache(self):
        """Will check the user omfg directory to see if the image already exists"""
        return self._cache == 1

    @property
    def chart_type(self):
        """Currently supports 'planview' and 'timeseries'."""
        return self._chart_type

    @property
    def column(self):
        """A Column object used for planview.  None for timeseries."""
        return self._column

    @property
    def cycle1(self):
        """Cycle object representing the first cycle time."""
        return self._cycle1

    @property
    def cycle2(self):
        """
        Cycle object representing the second cycle time.
        For planview, this will be the same as cycle1.
        """
        return self._cycle2

    @property
    def data_path(self):
        """pathlib.Path object for the path to the numpy data files"""
        return self._data_path

    @property
    def obs_group(self):
        """The obs group (e.g. aircraft, sonde, surface)"""
        return self._obs_group

    @property
    def varno(self):
        """The Varno object to be plotted"""
        return self._varno

    @property
    def vertco_max(self):
        """The maximum inclusive vertical coordinate level or channel"""
        return self._vertco_max

    @property
    def vertco_min(self):
        """The minimum inclusive vertical coordinate level or channel"""
        return self._vertco_min

    @property
    def vertco_type(self):
        """The VertcoType object selected."""
        return self._vertco_type

    @property
    def is_depar(self):
        """Returns true if the column is an_depar or fg_depar"""
        if self.column is not None:
            return self.column.is_depar
        return False

    def get_output_filestem(self):
        """Get the filename stem for the output chart"""
        filestem_parts = []
        for item in _FILESTEM_PROPERTIES:
            value = getattr(self, item)
            if value is not None:
                filestem_parts.append(str(value))
        return "_".join(filestem_parts)


    @staticmethod
    def load(json_file):
        """Create a Config object from a JSON file"""
        with open(json_file, "r") as fh_in:
            json_data = json.load(fh_in)
        return Config(**json_data)
