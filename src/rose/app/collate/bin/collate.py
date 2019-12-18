#!/usr/bin/env python3

"""Collates metadata from the output files generated by the collect app"""

import json
import logging
import os
from collections import defaultdict as ddict
from pathlib import Path
from py3odb.constants import Varno
import numpy as np
from omfg.app import BaseApp
from omfg.constants import VertcoType


class CollateApp(BaseApp):
    """Main program class"""
    def _run(self):
        """Run the app"""
        cycle = os.environ['CYLC_TASK_CYCLE_POINT']
        source_path = Path(os.environ['NP_DIRECTORY']) / cycle
        self.validate_directory(str(source_path))
        self._write_json(source_path, self._collate(source_path))

    @staticmethod
    def _collate(source_path):
        """Look through the numpy files and build a dictionary of metadata"""
        logging.info("Parsing through numpy files")
        data = ddict(dict)
        for source_file in source_path.glob("*.npy"):
            logging.info("Examining %s", source_file)
            obs_group, varno_code = source_file.stem.split("_")
            varno_code = int(varno_code)
            np_data = np.load(str(source_file))
            if len(np_data) == 0:
                continue
            varno_name = Varno.get_name(varno_code)
            data[obs_group][varno_code] = {
                'source_file': str(source_file),
                'length': len(np_data),
                'varno_name': varno_name,
                'varno_desc': Varno.get_desc(varno_name),
                'vertco_types': [int(x) for x in np.unique(np_data['vertco_type@body'])]
            }
            if VertcoType.CHANNEL_NUMBER in data[obs_group][varno_code]['vertco_types']:
                channel_indx = np.where(np_data['vertco_type@body'] == VertcoType.CHANNEL_NUMBER)
                channels = [
                    int(x) for x in np.unique(np_data['vertco_reference_1@body'][channel_indx])
                ]
                data[obs_group][varno_code]['channels'] = channels
        return data

    @staticmethod
    def _write_json(source_path, data):
        """Generate the JSON output file"""
        logging.info("Writing collated data to file")
        json_file = source_path / "collated.json"
        with json_file.open("w") as fh_out:
            json.dump(data, fh_out, indent=4, sort_keys=True)


def main():
    """Main function"""
    collate_app = CollateApp()
    collate_app.run()


if __name__ == "__main__":
    main()