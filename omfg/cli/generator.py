#!/usr/bin/env python3

"""Program interface for generating OMFG charts"""

from argparse import ArgumentParser
import json
import traceback
from omfg.chart.planview import Planview
from omfg.chart.timeseries import Timeseries


def get_args():
    """Get the command-line arguments"""
    parser = ArgumentParser()
    parser.add_argument("json_file", help="The JSON configuration file")
    return parser.parse_args()


def generate():
    """Call the appropriate chart generator"""
    args = get_args()
    with open(args.json_file, "r") as fh_in:
        config = json.load(fh_in)
    if config["chart_type"] == "planview":
        chart_generator = Planview(config)
    elif config["chart_type"] == "timeseries":
        chart_generator = Timeseries(config)
    else:
        raise ValueError(f"Unknown chart type: {config['chart_type']}")
    return chart_generator.generate()


if __name__ == "__main__":
    try:
        print(f"[OK]{generate()}")
    except Exception as err:
        traceback.print_exc()
        print(f"[FAIL]{err}")
