"""Plan View for generating map based charts"""

from pathlib import Path
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cartopy
from cartopy.feature import BORDERS
import cartopy.crs as ccrs
from .chart import Chart


class Planview(Chart):
    """Map-based chart"""
    cartopy.config["data_dir"] = str(Path(__file__).parent / "cartopy")

    def generate(self):
        """Generate the chart"""
        omfg_path = self.get_omfg_path()
        image_filepath = omfg_path / self.get_image_filename()
        if image_filepath.is_file():
            return str(image_filepath)
        map_ax = self.setup_map_ax()
        cmap, norm = self.setup_colors()
        lats, lons, data = self.load_data(Path(self.config["data_path"]))
        self.generate_plot(str(image_filepath), map_ax, cmap, norm, lons, lats, data)
        return str(image_filepath)

    def get_image_filename(self):
        """Get the image filename"""
        vertco_min, vertco_max = self.config["vertco"].split(",")
        filestem = "_".join([
            self.config["chart_type"],
            self.config["cycle"],
            self.config["column"],
            self.config["varno"],
            self.config["obs_group"],
            str(self.config["vertco_type"]),
            vertco_min,
            vertco_max
        ])
        return f"{filestem}.png"

    @staticmethod
    def setup_map_ax():
        """Set up the map axis"""
        logging.info("Setting up map axis")
        map_ax = plt.axes([0.1, 0.15, 0.8, 0.7], projection=ccrs.PlateCarree())
        map_ax.set_global()
        map_ax.coastlines()
        map_ax.add_feature(BORDERS)
        map_gl = map_ax.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=1,
            alpha=0.25,
            color="gray"
        )
        # map_gl.xlabels_top = False  # cartopy <= 0.17
        map_gl.top_labels = False
        return map_ax

    @staticmethod
    def setup_colors():
        """Set up the color related stuff"""
        logging.info("Normalizing colors")
        cmap = mpl.cm.get_cmap("jet")
        bounds = np.arange(950, 1060, 10)  # TODO: make this dynamic based on chart details
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        return cmap, norm

    def load_data(self, data_path):
        """Use numpy to load the data"""
        numpy_filepath = data_path / self.config["cycle"]
        numpy_filepath /= f"{self.config['obs_group']}_{self.config['varno']}.npy"
        logging.info("Loading the numpy data")
        np_data = np.load(str(numpy_filepath))
        logging.info("Extracting the relevant data")
        column = self.config["column"]
        vertco_min, vertco_max = self.config["vertco"].split(",")
        condition = (~np.isnan(np_data[column]))
        condition &= (~np.isnan(np_data["vertco_reference_1@body"]))
        condition &= (np_data["vertco_type@body"] == int(self.config["vertco_type"]))
        # condition &= (np_data["vertco_reference_1@body"] >= np.float(vertco_min))
        # condition &= (np_data["vertco_reference_1@body"] <= np.float(vertco_max))
        indx = np.where(condition)
        lats = np_data["lat@hdr"][indx]
        lons = np_data["lon@hdr"][indx]
        data = np_data[column][indx]
        data /= 100.0  # TODO: make this dynamic based on chart details
        return lats, lons, data

    def generate_plot(self, filename, map_ax, cmap, norm, lons, lats, data):
        """Generate the plot"""
        logging.info("Generating scatter plot")
        sc_plot = map_ax.scatter(
            lons,
            lats,
            transform=ccrs.PlateCarree(),
            c=data,
            s=1.0,
            cmap=cmap,
            norm=norm
        )

        logging.info("Adding colorbar")
        cbar_ax = plt.axes([0.10, 0.125, 0.8, 0.025])
        cbar = self.figure.colorbar(sc_plot, cax=cbar_ax, orientation="horizontal")
        cbar.ax.tick_params(size=0)

        logging.info("Adding textbox")
        text_ax = plt.axes([0.1, 0.8, 0.8, 0.05])
        text_ax.get_xaxis().set_ticks([])
        text_ax.get_yaxis().set_ticks([])
        text_ax.text(0.05, 0.35, f"Obs Count: {len(data)}", fontsize=10)
        text_ax.text(0.25, 0.35, f"Max: {np.max(data):.1f}", fontsize=10)
        text_ax.text(0.45, 0.35, f"Min: {np.min(data):.1f}", fontsize=10)
        text_ax.text(0.65, 0.35, f"Mean: {np.mean(data):.1f}", fontsize=10)
        text_ax.text(0.85, 0.35, f"StDev: {np.std(data):.1f}", fontsize=10)
        text_ax.set_title(
            f"{'Mean sea-level pressure (hPa): an_depar':100}20190917T0600Z",
            fontsize=14
        )
        logging.info("Saving")
        plt.savefig(filename, bbox_inches="tight", dpi=100, pad_inches=0.25)
