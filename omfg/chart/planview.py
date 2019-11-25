"""Plan View for generating map based charts"""

from pathlib import Path
import logging
import matplotlib as mpl
# pylint: disable=wrong-import-position,wrong-import-order
mpl.use("AGG")
import matplotlib.pyplot as plt
import numpy as np
import cartopy
from cartopy.feature import BORDERS
import cartopy.crs as ccrs

from .chart import Chart


class Planview(Chart):
    """Map-based chart"""
    logging.info("Telling cartopy to use data_dir: %s", str(Path(__file__).parent / "cartopy"))
    cartopy.config["data_dir"] = str(Path(__file__).parent / "cartopy")

    def _generate(self):
        """Generate the chart"""
        logging.info("Generating chart")
        lats, lons, data = self.load_data()
        if self.config.varno.formula is not None:
            if self.config.is_depar:
                data = eval(self.config.varno.formula["depar"])
            else:
                data = eval(self.config.varno.formula["value"])
        map_ax = self.setup_map_ax()
        cmap, norm = self.setup_colors(np.min(data), np.max(data))
        self.generate_plot(map_ax, cmap, norm, lons, lats, data)

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
        # cartopy is weird about turning off the top labels
        # which appears to have changed with 0.17
        map_gl.xlabels_top = False  # cartopy <= 0.17
        map_gl.top_labels = False
        return map_ax

    def setup_colors(self, min_value, max_value):
        """Set up the color related stuff"""
        logging.info("Normalizing colors")
        if self.config.varno.cmap is not None:
            if self.config.is_depar:
                cmap = mpl.cm.get_cmap(self.config.varno.cmap["depar"])
            else:
                cmap = mpl.cm.get_cmap(self.config.varno.cmap["value"])
        else:
            cmap = mpl.cm.get_cmap("jet")
        if self.config.varno.levels is None:
            bounds = np.linspace(min_value, max_value, 10)
        else:
            if self.config.is_depar:
                bounds = self.config.varno.levels["depar"]
            else:
                bounds = self.config.varno.levels["value"]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        return cmap, norm

    def load_data(self):
        """Use numpy to load the data"""
        numpy_filepath = self.config.data_path / str(self.config.cycle1)
        numpy_filepath /= f"{self.config.obs_group}_{self.config.varno.code}.npy"
        logging.info("Loading the numpy data")
        np_data = np.load(str(numpy_filepath))
        logging.info("Extracting the relevant data")
        condition = (~np.isnan(np_data[self.config.column.name]))
        condition &= (~np.isnan(np_data["vertco_reference_1@body"]))
        condition &= (np_data["vertco_type@body"] == self.config.vertco_type.code)
        condition &= (np_data["vertco_reference_1@body"] >= self.config.vertco_min)
        condition &= (np_data["vertco_reference_1@body"] <= self.config.vertco_max)
        indx = np.where(condition)
        lats = np_data["lat@hdr"][indx]
        lons = np_data["lon@hdr"][indx]
        data = np_data[self.config.column.name][indx]
        return lats, lons, data

    def generate_plot(self, map_ax, cmap, norm, lons, lats, data):
        """Generate the plot"""
        # pylint: disable=too-many-arguments
        logging.info("Generating scatter plot")
        sc_plot = map_ax.scatter(
            lons,
            lats,
            c=data,
            s=1.0,
            # marker="o",
            cmap=cmap,
            norm=norm
        )

        logging.info("Adding colorbar")
        cbar_ax = plt.axes([0.10, 0.125, 0.8, 0.025])
        cbar = self.figure.colorbar(sc_plot, cax=cbar_ax, orientation="horizontal")
        if self.config.varno.units is not None:
            cbar.set_label(self.config.varno.units)
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
            self.get_title(),
            fontsize=14
        )
        logging.info("Saving")
        plt.savefig(str(self.output_filepath), bbox_inches="tight", dpi=150, pad_inches=0.25)

    def get_vertco_label(self):
        """Get a string representing the vertco type/range"""
        vertco = f'{self.config.vertco_type.label}: '
        vertco += f'{int(self.config.vertco_min)}'
        if self.config.vertco_min != self.config.vertco_max:
            vertco += f' - {int(self.config.vertco_max)}'
        return vertco

    def get_varno_desc(self):
        """Get a string representing the varno description and column if applicable"""
        description = self.config.varno.desc
        column_title = self.config.column.label
        if column_title is not None:
            description += f" ({column_title})"
        return description

    def get_title(self):
        """Build the title for the chart"""
        title = f'Obs Group: {self.config.obs_group:25}{self.get_vertco_label():>46}\n'
        title += f'{self.get_varno_desc():68}{self.config.cycle1}'
        return title
