"""Import to add project directory to PYTHONPATH"""
import pathlib
import sys


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
# pylint: disable=wrong-import-position,unused-import
import omfg # noqa: 401,402
import omfg.chart as chart # noqa: 401,402
import omfg.wrappers as wrappers # noqa: 401,402
