"""Module for inheritable base rose/cylc app"""

import abc
import argparse
import os
import logging
import pathlib
import shutil
import socket
import sys
import traceback
from datetime import datetime as dt
from omfg.util import StopWatch


DEFAULT_LOG_LEVEL = logging.INFO

_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    None: DEFAULT_LOG_LEVEL
}


class BaseApp(abc.ABC):
    """
    Abstract class for running a GALWEM related rose/cylc app.
    If you want to allow setting the log level from the command-line,
    make sure to include a switch with a long argument name of 'loglevel'.
    """
    def __init__(self, pos_args=None, opt_args=None):
        self._pos_args = pos_args
        self._opt_args = opt_args
        self._args = self._parse(pos_args, opt_args)
        self._log_level = self._get_log_level()
        self._init_logging()

    def _get_log_level(self):
        """Determine the logging level"""
        try:
            return _LOG_LEVELS[self.get_arg("loglevel")]
        except KeyError:
            return DEFAULT_LOG_LEVEL

    def _init_logging(self):
        """Initialize logging however you see fit"""
        root_logger = logging.getLogger('')
        root_logger.handlers = []  # remove existing handlers
        root_logger.setLevel(logging.DEBUG)  # minimum log level for all handlers
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self._log_level)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(message)s",
            "%Y-%m-%dT%H:%M:%SZ"
        )
        stdout_handler.setFormatter(formatter)
        root_logger.addHandler(stdout_handler)

    def _log_args(self):
        """Log the values of the command-line arguments"""
        logging.info("Command line options:")
        if self._pos_args is not None:
            for keyname, _, _ in self._pos_args:
                logging.info("%-20s = %s", keyname, self.get_arg(keyname))
        if self._opt_args is not None:
            for _, keyname, _, _ in self._opt_args:
                logging.info("%-20s = %s", keyname, self.get_arg(keyname))

    @staticmethod
    def _parse(pos_args, opt_args):
        """
        Parse command-line arguments into dictionary.

        The standard argparse library isn't terribly difficult to use, but this
        function allows for positional and optional arguments to be defined
        up-front without having to worry about how to call argparse.  The effect
        should be an easy standardization for how arguments are parsed.

        Note that if you include positional arguments, they will be required and
        based on position.  Optional arguments require both short and long names
        and can either take a value or act as a boolean flag.

        The list of positional arguments should contain:
            argument name, help text, argument type (e.g. int, str)

        The list of optional arguments contains:
            short name, long name, help text, argument type (e.g. int, bool)

        Args:
            pos_args ([str, str, type])     : List of positional arguments
            opt_args ([str, str, str, type]): List of optional arguments

        Returns:
            (dict): A dictionary with either the arg_name or long_opt as key
                    and associated input as the value.
        """
        parser = argparse.ArgumentParser()
        if pos_args is not None:
            for argument_name, help_text, argument_type in pos_args:
                parser.add_argument(
                    argument_name,
                    help=help_text,
                    type=argument_type
                )
        if opt_args is not None:
            for short_name, long_name, help_text, argument_type in opt_args:
                kwargs = {
                    "dest": long_name,
                    "help": help_text
                }
                if argument_type == bool:
                    kwargs["action"] = "store_true"
                    kwargs["default"] = False
                else:
                    kwargs["type"] = argument_type
                parser.add_argument(
                    f"-{short_name}",
                    f"--{long_name}",
                    **kwargs
                )
        return vars(parser.parse_args())

    @abc.abstractmethod
    def _run(self):
        """Subclasses must implement this method for the main program logic"""
        raise NotImplementedError()

    def get_arg(self, argument_name):
        """Returns the value for the given argument name or None if not available"""
        try:
            return self._args[argument_name]
        except KeyError:
            return None

    @staticmethod
    def get_hostname():
        """Return the system's hostname"""
        return socket.gethostname()

    @staticmethod
    def get_timestamp():
        """Get a simple Y-m-dTH:M:SZ timestamp"""
        return f"{dt.now():%Y-%m-%dT%H:%M:%SZ}"

    @staticmethod
    def prepare_directory(directory, destroy=False):
        """Prepare a directory.  Remove the and remake directory if destroy is on."""
        dir_path = pathlib.Path(directory)
        error_message = f"Could not prepare directory {dir_path}: "
        if dir_path.is_file():
            raise OSError(f"{error_message}: already exists as a file")
        if destroy and dir_path.is_dir():
            try:
                shutil.rmtree(str(dir_path))
            except OSError as err:
                raise OSError(f"{error_message}: {err.strerror}")
        try:
            dir_path.mkdir(exist_ok=True)
        except OSError as err:
            raise OSError(f"{error_message}: {err.strerror}")

    def run(self):
        """This method should be used to execute the script"""
        try:
            watch = StopWatch()
            self._run()
            watch.mark()
            logging.info("Total elapsed time: %s", watch.get_total_elapsed())
        except Exception as err:
            traceback.print_exc()
            logging.error("Exiting on error: %s", err)
            raise SystemExit(1)

    def run_unique(self, unique_name):
        """Only run one instance of this script"""
        logging.info("Trying to create unique socket: %s", unique_name)
        try:
            unique_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            unique_socket.bind(f"\0{unique_name}")
            self.run()
        except (OSError, socket.error):
            logging.warning("Unique process %s already exists, exiting", unique_name)
            raise SystemExit(0)

    @staticmethod
    def validate_directory(directory):
        """
        A simple path validation.  This function fixes the path manipulation Fortify
        finding.  The paths passed in as environment variables need to be validated
        before they are used.
        """
        if not os.path.isdir(directory):
            raise OSError(f"Cannot validate directory {directory}: no such directory")
