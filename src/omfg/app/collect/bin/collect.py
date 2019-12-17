#!/usr/bin/env python3

"""App for collecting data from odb files into numpy files"""

import logging
import os
from pathlib import Path
import numpy as np
from omfg.app import BaseApp
from omfg.wrappers import ODB


class CollectApp(BaseApp):
    """Main program class"""
    def _run(self):
        """Run the app"""
        config = self._get_config()
        self.prepare_directory(config['target_path'], destroy=False)
        self._collect(config)

    @staticmethod
    def _collect(config):
        """Extract data and generate the output file"""
        target_file = config['target_path'] / f"{config['source_type']}_{config['varno']}.npy"
        if target_file.is_file() and not config["overwrite"]:
            logging.info("Target file exists, will not generate")
            return
        odb = ODB(
            filename=str(config['source_path'] / f"{config['source_type']}.odb"),
            varno=config['varno'],
            include_rejects=config['include_rejects']
        )
        odb.save_numpy(config['varno'], str(target_file))
        logging.info("Validating numpy file")
        data = np.load(str(target_file))
        logging.info("Loaded %s entries", len(data))

    @staticmethod
    def _get_config():
        """Build a dictionary with the necessary configuration info"""
        config = {}
        cycle = os.environ['CYLC_TASK_CYCLE_POINT']
        config['source_path'] = Path(os.environ['ODB2_DIRECTORY']) / cycle
        config['target_path'] = Path(os.environ['NP_DIRECTORY']) / cycle
        config['source_type'] = os.environ['SOURCE_TYPE']
        config['varno'] = int(os.environ['VARNO'])
        config['include_rejects'] = int(os.environ['INCLUDE_REJECTS']) > 0
        config['overwrite'] = int(os.environ['OVERWRITE']) > 0
        logging.info("Environment Configuration:")
        for keyname, value in config.items():
            logging.info("  %15s: %s", keyname, value)
        return config


def main():
    """Main function"""
    collect_app = CollectApp()
    collect_app.run()


if __name__ == "__main__":
    main()
