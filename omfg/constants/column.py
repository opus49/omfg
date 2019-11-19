"""Module for handling column names for label purposes"""


class Column:
    @staticmethod
    def get_title(column):
        try:
            return COLUMN_TITLES[column]
        except KeyError:
            return None


COLUMN_TITLES = {
    "obsvalue@body": None,
    "corvalue@body": "Corrected",
    "an_depar@body": "O-A",
    "fg_depar@body": "O-B"
}
