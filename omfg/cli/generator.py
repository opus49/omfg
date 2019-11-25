#!/usr/bin/env python3

"""Program interface for generating OMFG charts"""

from argparse import ArgumentParser
import logging
import traceback

from omfg.util import init_logging
from omfg.chart import Config, Planview, Timeseries


def get_args():
    """Get the command-line arguments"""
    parser = ArgumentParser()
    parser.add_argument("json_file", help="The JSON configuration file")
    return parser.parse_args()


def generate():
    """Call the appropriate chart generator"""
    args = get_args()
    config = Config.load(args.json_file)
    if config.chart_type == "planview":
        chart_generator = Planview(config)
    elif config.chart_type == "timeseries":
        chart_generator = Timeseries(config)
    else:
        raise ValueError(f"Unknown chart type: {config.chart_type}")
    return chart_generator.generate()


def main():
    """Main program"""
    init_logging(logging.INFO)
    try:
        print(f"[OK]{generate()}")
    except Exception as err:
        traceback.print_exc()
        print(f"[FAIL]{err}")


if __name__ == "__main__":
    main()
