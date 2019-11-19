"""Plan View for generating map based charts"""

from pathlib import Path
import logging
import matplotlib as mpl
mpl.use("AGG")
import matplotlib.pyplot as plt
import numpy as np
import cartopy
from cartopy.feature import BORDERS
import cartopy.crs as ccrs
from .chart import Chart
from omfg.constants import Column, Varno, VertcoType


class Planview(Chart):
    """Map-based chart"""
    logging.info("Telling cartopy to use data directory: %s", str(Path(__file__).parent / "cartopy"))
    cartopy.config["data_dir"] = str(Path(__file__).parent / "cartopy")

    def generate(self):
        """Generate the chart"""
        mpl.rcParams["font.sans-serif"] = "Noto Mono"
        mpl.rcParams["font.family"] = "sans-serif"
        logging.info("Generating chart")
        omfg_path = self.get_omfg_path()
        image_filepath = omfg_path / self.get_image_filename()
        if self.config["cache"] == "true":
            if image_filepath.is_file():
                return str(image_filepath)
        self.varno = Varno.get_varno_from_code(self.config["varno"])
        lats, lons, data = self.load_data()
        if self.varno.formula is not None:
            if "depar" in self.config["column"]:
                data = eval(self.varno.formula["depar"])
            else:
                data = eval(self.varno.formula["value"])
        map_ax = self.setup_map_ax()
        cmap, norm = self.setup_colors(np.min(data), np.max(data))
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
        # cartopy is weird about turning off the top labels
        # which appears to have changed with 0.17
        map_gl.xlabels_top = False  # cartopy <= 0.17
        map_gl.top_labels = False
        return map_ax

    def setup_colors(self, min_value, max_value):
        """Set up the color related stuff"""
        logging.info("Normalizing colors")
        if self.varno.cmap is not None:
            if "depar" in self.config["column"]:
                cmap = mpl.cm.get_cmap(self.varno.cmap["depar"])
            else:
                cmap = mpl.cm.get_cmap(self.varno.cmap["value"])
        else:
            cmap = mpl.cm.get_cmap("jet")
        # bounds = np.arange(950, 1060, 10)  # TODO: make this dynamic based on chart details
        if self.varno.levels is None:
            bounds = np.linspace(min_value, max_value, 10)
        else:
            if "depar" in self.config["column"]:
                bounds = self.varno.levels["depar"]
            else:
                bounds = self.varno.levels["value"]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        return cmap, norm

    def load_data(self):
        """Use numpy to load the data"""
        data_path = Path(self.config["data_path"])
        numpy_filepath = data_path / self.config["cycle"]
        numpy_filepath /= f"{self.config['obs_group']}_{self.config['varno']}.npy"
        logging.info("Loading the numpy data")
        np_data = np.load(str(numpy_filepath))
        logging.info("Extracting the relevant data")
        column = self.config["column"]
        vertco_min, vertco_max = self.get_vertco_bounds()
        condition = (~np.isnan(np_data[column]))
        condition &= (~np.isnan(np_data["vertco_reference_1@body"]))
        condition &= (np_data["vertco_type@body"] == int(self.config["vertco_type"]))
        condition &= (np_data["vertco_reference_1@body"] >= vertco_min)
        condition &= (np_data["vertco_reference_1@body"] <= vertco_max)
        indx = np.where(condition)
        lats = np_data["lat@hdr"][indx]
        lons = np_data["lon@hdr"][indx]
        data = np_data[column][indx]
        return lats, lons, data

    def generate_plot(self, filename, map_ax, cmap, norm, lons, lats, data):
        """Generate the plot"""
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
        if self.varno.units is not None:
            cbar.set_label(self.varno.units)
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
        plt.savefig(filename, bbox_inches="tight", dpi=150, pad_inches=0.25)

    def get_vertco_bounds(self):
        """Get the min/max vertco reference values as numpy floating values"""
        vertco_min, vertco_max = self.config["vertco"].split(",")
        return np.float(vertco_min), np.float(vertco_max)

    def get_vertco(self):
        """Get a string representing the vertco type/range"""
        vertco = f'{VertcoType.get_type(self.config["vertco_type"])}: '
        vertco_min, vertco_max = self.get_vertco_bounds()
        vertco += f'{int(vertco_min)}'
        if vertco_min != vertco_max:
            vertco += f' - {int(vertco_max)}'
        return vertco

    def get_desc(self):
        """Get a string representing the varno description and column if applicable"""
        description = Varno.get_desc(Varno.get_name(self.config["varno"]))
        column_title = Column.get_title(self.config["column"])
        if column_title is not None:
            description += f" ({column_title})"
        return description

    def get_title(self):
        """Build the title for the chart"""
        title = f'Obs Group: {self.config["obs_group"]:25}{self.get_vertco():>46}\n'
        title += f'{self.get_desc():68}{self.config["cycle"]}'
        return title
