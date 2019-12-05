"""Groups varnos for the planview chart generator options"""


class VarnoType:
    """Class for grouping varnos by similar characteristics"""
    def __init__(self, cmap=None, formula=None, levels=None, units=None):
        self._cmap = cmap
        self._formula = formula
        self._levels = levels
        self._units = units

    @property
    def cmap(self):
        """The colormap"""
        return self._cmap

    @property
    def formula(self):
        """The formula to be applied to this type of varno"""
        return self._formula

    @property
    def levels(self):
        """The colorbar levels that apply to this type of varno"""
        return self._levels

    @property
    def units(self):
        """The units that apply to this type of varno after the formula is applied"""
        return self._units

    @staticmethod
    def from_type(varno_type):
        """Get a varno type object from the given varno type name"""
        if varno_type in VARNO_TYPES:
            return VarnoType(
                cmap=VARNO_TYPES[varno_type]["cmap"],
                formula=VARNO_TYPES[varno_type]["formula"],
                levels=VARNO_TYPES[varno_type]["levels"],
                units=VARNO_TYPES[varno_type]["units"]
            )
        raise ValueError(f"Unknown varno type: {varno_type}")


VARNO_TYPES = {
    "pressure": {
        "cmap": {
            "depar": "bwr",
            "value": "jet"
        },
        "formula": {
            "depar": "data / 100",
            "value": "data / 100"
        },
        "levels": {
            "depar": (-50, -20, -10, -5, -2.5, 0, 2.5, 5, 10, 20, 50),
            "value": (850, 860, 870, 880, 890, 900, 910, 920, 930, 940)
        },
        "units": "hPa",
    },
    "temperature": {
        "cmap": {
            "depar": "bwr",
            "value": "jet"
        },
        "formula": {
            "depar": "data",
            "value": "data - 273.15"
        },
        "levels": {
            "depar": (-50, -20, -10, -5, -2.5, 0, 2.5, 5, 10, 20, 50),
            "value": (-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40)
        },
        "units": "Degrees Celsius"
    }
}
