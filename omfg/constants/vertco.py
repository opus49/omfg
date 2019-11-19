"""Module for vertical coordinates"""

class VertcoType:
    @staticmethod
    def get_type(code):
        try:
            return VERTCO_TYPES[int(code)]
        except KeyError:
            return "unknown"


VERTCO_TYPES = {
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
