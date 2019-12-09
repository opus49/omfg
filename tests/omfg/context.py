"""Import to add project directory to PYTHONPATH"""
import pathlib
import sys


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "src"))
import omfg  # noqa: 401,402 # pylint: disable=wrong-import-position,unused-import
