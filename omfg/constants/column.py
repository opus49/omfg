"""Module for handling column names for label purposes"""

COLUMN_LABELS = {
    "obsvalue@body": None,
    "corvalue@body": "Corrected",
    "an_depar@body": "O-A",
    "fg_depar@body": "O-B"
}


class Column:
    """A column object"""
    def __init__(self, name, label):
        self._name = name
        self._label = label

    def __str__(self):
        parts = self._name.split("@")
        return parts[0]

    @property
    def name(self):
        """The name used by ODB2"""
        return self._name

    @property
    def label(self):
        """The label used by chart generators"""
        return self._label

    @property
    def is_depar(self):
        """True if the column is an_depar or fg_depar"""
        return "depar" in self.name

    @staticmethod
    def get_column(name):
        """Static method for creating Column objects"""
        try:
            return Column(name=name, label=COLUMN_LABELS[name])
        except KeyError:
            raise ValueError(f"Unknown column name {name}")
