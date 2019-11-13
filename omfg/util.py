"""Utility module"""

import logging


def init_logging(level=logging.INFO):
    """Initialize simple logging because I'm tired of looking up the syntax """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
