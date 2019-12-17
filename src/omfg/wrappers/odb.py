"""
Wrapper for odb2 files.  Use to extract specific data and save it in different formats.
"""

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

# at least one of these fields must be present
_MANDATORY_FIELDS = {
    "corvalue@body",
    "obsvalue@body"
}


class ODB:
    """
    Object wrapper around the relevant data contained in an odb2 file.
    If you do not specify a varno, all varnos will be extracted.  The
    fields argument should be a dictionary where the key is the column
    name and the value is the numpy data type.
    """
    def __init__(self, filename, varno=None, fields=None, include_rejects=False):
        self._fields = fields if fields is not None else _DEFAULT_FIELDS
        self._include_rejects = include_rejects
        self._data = self._read_odb(filename, varno)

    @property
    def varnos(self):
        """Get an array of varnos"""
        return np.unique(self._data["varno@body"])

    def get_varno_data(self, varno):
        """Get a numpy array subset for the given varno"""
        return self._data[self._get_varno_index(varno)]

    def save_numpy(self, varno, filename):
        """Save the numpy data for the given varno to the referenced numpy file"""
        logging.info("Saving Numpy file")
        np.save(filename, self.get_varno_data(varno))

    def _build_dtype(self):
        """Build a numpy dtype from the fields"""
        return np.dtype(list(self._fields.items()))

    def _get_conditional(self, varno):
        """Get the WHERE conditional for the SQL query"""
        conditions = [f"({' OR '.join(_MANDATORY_FIELDS)})"]
        if varno is not None:
            conditions.append(f"varno={varno}")
        if not self._include_rejects:
            conditions.append("report_status.active")
        return " AND ".join(conditions)

    def _get_varno_index(self, varno):
        """Get the numpy index to the referenced varno"""
        return np.where(self._data["varno@body"] == varno)

    def _read_odb(self, filename, varno):
        """Read the database and generate a numpy array"""
        logging.info("Extracting data from %s", filename)
        rows = []
        sql_command = f"SELECT {','.join(self._fields.keys())} FROM <odb>"
        conditional = self._get_conditional(varno)
        if conditional:
            sql_command += f" WHERE {conditional}"
        logging.debug("sql_command: %s", sql_command)
        with Reader(filename, sql_command) as odb_reader:
            for row in odb_reader:
                rows.append(tuple(row))
        logging.info("Generating numpy array")
        return np.array(rows, dtype=self._build_dtype())
