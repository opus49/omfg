"""Module for vertical coordinates"""


VERTCO_LABELS = {
    1: "Pressure",
    2: "Geopotential Height",
    3: "TOVS Channel",
    4: "Scatterometer Channel",
    5: "Model Level Number",
    6: "Impact Parameter",
    7: "Channel Number",
    8: "Channel Wavelength",
    9: "Channel Frequency",
    10: "Ocean Depth",
    11: "Derived Pressure",
    12: "Ambivalent Wind Number",
    13: "Tangent Height for SBUV",
    14: "Model Level Pressure",
    15: "Lidar Range",
    16: "Lane Number"
}


class VertcoType:
    """A type of vertical coordinate"""
    def __init__(self, code, label):
        self._code = code
        self._label = label

    def __str__(self):
        return f"{self.code}"

    @property
    def code(self):
        """The integer value used by ODB2"""
        return self._code

    @property
    def label(self):
        """The label used by chart generators"""
        return self._label

    @staticmethod
    def get_vertco_type(code):
        """Get a VertcoType object from a code"""
        try:
            return VertcoType(code=code, label=VERTCO_LABELS[int(code)])
        except (KeyError, ValueError) as err:
            raise ValueError(f"Invalid code {code}: {err}")
