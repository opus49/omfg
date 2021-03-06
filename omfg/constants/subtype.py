"""Constant values for the OPS SUBTYPE column from ODB2 files"""


class Subtype:
    """Static class for looking up OPS SUBTYPE information."""
    @staticmethod
    def get_name(subtype_code):
        """Retrieve the subtype name for the given code"""
        for name, code in OPS_SUBTYPES.items():
            if code == subtype_code:
                return name
        return None

    @staticmethod
    def get_code(subtype_name):
        """Retrieve the subtype code for the given name"""
        try:
            return OPS_SUBTYPES[subtype_name]
        except KeyError:
            return None


OPS_SUBTYPES = {
    "aatsr": 20400,
    "aireps": 30200,
    "airqal": 11000,
    "airqaleu": 11001,
    "airs": 22800,
    "airsl": 25100,
    "airsms": 24700,
    "airsrr": 23900,
    "airswf": 24000,
    "aladin": 20700,
    "amdars": 30100,
    "amsr2": 25000,
    "amsub": 23200,
    "argo": 60202,
    "ascat": 24300,
    "ascatco": 26700,
    "ascathr": 25500,
    "atdnet": 11300,
    "atms": 21800,
    "atmshr": 21900,
    "atovsg": 21400,
    "atovsl": 21500,
    "bathy": 60100,
    "bogus": 40300,
    "buoy": 11700,
    "buoyprof": 60300,
    "cmawinds": 24900,
    "comscsr": 26200,
    "crimss": 26000,
    "crimsshr": 26100,
    "dropsond": 50300,
    "drwind": 10601,
    "esacmw": 22200,
    "esacsr": 25700,
    "esacswvw": 22300,
    "esahrvw": 22100,
    "esahrwvw": 22400,
    "esaura": 20100,
    "esauwa": 20200,
    "esauwi": 20500,
    "fy3b": 21450,
    "gauge": 10401,
    "ghrsst": 24400,
    "gmi": 29100,
    "goesamw": 22000,
    "goesbufr": 22500,
    "goescsr": 25800,
    "goesvis": 22002,
    "goeswv": 22003,
    "gpsiwv": 21700,
    "gpsro": 22900,
    "himcsr": 26310,
    "himrad": 26320,
    "hrseaice": 60600,
    "iasig": 24100,
    "iasihr": 25300,
    "iasil": 24200,
    "imdwinds": 25200,
    "ind3d": 26900,
    "jmacsr": 26300,
    "jmawinds": 23500,
    "kmawinds": 25900,
    "lidar": 11501,
    "lndsyb": 11600,
    "lndsyn": 10100,
    "meris": 25400,
    "metars": 11100,
    "mobsyn": 10800,
    "modes": 30500,
    "modis": 22600,
    "msgaod": 25600,
    "msgcsr": 24500,
    "msgctp": 24660,
    "msgctpfd": 24680,
    "msgctpuk": 24670,
    "msgrad": 24600,
    "msgradfd": 24650,
    "msgraduk": 24610,
    "msgwinds": 23600,
    "mwri": 29000,
    "mwts": 27000,
    "oceanfb": 60401,
    "oceanre": 60402,
    "oceants": 60403,
    "openroad": 10900,
    "osseaice": 60500,
    "ozonesat": 23700,
    "paobs": 40700,
    "pilot": 50200,
    "radop": 10604,
    "radop2": 10605,
    "radrefl": 10602,
    "radrefr": 10606,
    "radrrate": 10400,
    "radvel": 10607,
    "rpbogus": 40500,
    "saphir": 28000,
    "saltssh": 23000,
    "saltsshs": 23002,
    "saltssht": 23001,
    "sataod": 26600,
    "satob": 21000,
    "sstbogus": 40200,
    "seawinds": 20300,
    "sferics": 11200,
    "shpsyn": 10200,
    "sonde": 50500,
    "srew": 10500,
    "ssmi": 21600,
    "ssmis": 23100,
    "stereomv": 27100,
    "tamdar": 30300,
    "tcbogus": 40100,
    "tcrtemp": 22700,
    "temp": 50100,
    "tesac": 60200,
    "thbogus": 40600,
    "tovsg": 21100,
    "tstsonde": 50501,
    "ukmosst": 20600,
    "ukwinds": 26400,
    "wavenet": 10700,
    "windsat": 24800,
    "winpro": 50400,
    "wisdom": 30400,
    "wow": 11400
}
