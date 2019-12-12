"""Wrapper for ODB files"""

import logging
import numpy as np
from py3odb import Reader


_DEFAULT_FIELDS = {
    "lat@hdr": "f8",
    "lon@hdr": "f8",
    "report_status@hdr": "i4",
    "an_depar@body": "f8",
    "corvalue@body": "f8",
    "fg_depar@body": "f8",
    "obsvalue@body": "f8",
    "ops_obstype@hdr": "i4",
    "varno@body": "i4",
    "vertco_reference_1@body": "f8",
    "vertco_reference_2@body": "f8",
    "vertco_type@body": "i4"
}


class ODB:
    """
    Object wrapper around the relevant data contained in an odb2 file.
    If you do not specify a varno, all varnos will be extracted.
    """
    def __init__(self, filename, varno=None, fields=None):
        if fields is None:
            fields = _DEFAULT_FIELDS
        self._data = self._read_odb(filename, varno, fields)

    @property
    def varnos(self):
        """Get an array of varnos"""
        return np.unique(self._data["varno@body"])

    def get_varno_data(self, varno):
        """Get a numpy array subset for the given varno"""
        return self._data[self._get_varno_index(varno)]

    @staticmethod
    def _build_dtype(fields):
        """Build a numpy dtype from the fields"""
        return np.dtype(list(fields.items()))

    def _get_varno_index(self, varno):
        """Get the numpy index to the referenced varno"""
        return np.where(self._data["varno@body"] == varno)

    def _read_odb(self, filename, varno, fields):
        """Read the database and generate a numpy array"""
        logging.info("Extracting data from odb file")
        rows = []
        sql_command = f"SELECT {','.join(fields.keys())} FROM <odb>"
        if varno is not None:
            sql_command += f" WHERE varno={varno}"
        with Reader(filename, sql_command) as odb_reader:
            for row in odb_reader:
                rows.append(tuple(row))
        logging.info("Generating numpy array")
        return np.array(rows, dtype=self._build_dtype(fields))
