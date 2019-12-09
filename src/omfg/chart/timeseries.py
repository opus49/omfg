"""Time series for generating map based charts"""

from collections import defaultdict as ddict
from copy import copy
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from .chart import Chart


class _TimeseriesData:
    def __init__(self, config):
        self._data = self._populate(config)

    @property
    def cycle_dates(self):
        """A list of Datetime objects for each cycle"""
        return self._data["cycle_dates"]

    @property
    def an_depar(self):
        """A list of mean an_depar values"""
        return self._data["an_depar"]

    @property
    def an_depar_std(self):
        """A list of mean an_depar standard deviation values"""
        return self._data["an_depar_std"]

    @property
    def fg_depar(self):
        """A list of mean fg_depar values"""
        return self._data["fg_depar"]

    @property
    def fg_depar_std(self):
        """A list of mean fg_depar standard deviation values"""
        return self._data["fg_depar_std"]

    @property
    def obscount(self):
        """A list of observation counts for each cycle"""
        return self._data["obscount"]

    @staticmethod
    def _populate(config):
        data = ddict(list)
        this_cycle = copy(config.cycle1)
        while this_cycle <= config.cycle2:
            np_file = config.data_path / str(this_cycle)
            np_file /= f"{config.obs_group}_{config.varno.code}.npy"
            if np_file.is_file():
                np_data = np.load(str(np_file))
                condition = (~np.isnan(np_data["obsvalue@body"]))
                condition &= (~np.isnan(np_data["vertco_reference_1@body"]))
                condition &= (np_data["vertco_type@body"] == config.vertco_type.code)
                condition &= (np_data["vertco_reference_1@body"] >= config.vertco_min)
                condition &= (np_data["vertco_reference_1@body"] <= config.vertco_max)
                indx = np.where(condition)
                data["cycle_dates"].append(this_cycle.datetime)
                data["an_depar"].append(np.mean(np_data["an_depar@body"][indx]))
                data["fg_depar"].append(np.mean(np_data["fg_depar@body"][indx]))
                data["an_depar_std"].append(np.std(np_data["an_depar@body"][indx]))
                data["fg_depar_std"].append(np.std(np_data["fg_depar@body"][indx]))
                data["obscount"].append(len(indx[0]))
            this_cycle.increment()
        return data


class Timeseries(Chart):
    """Time-series based chart"""
    def _generate(self):
        """Generate the chart"""
        data = _TimeseriesData(self.config)
        plt.subplots_adjust(hspace=0.4)
        ax1 = plt.subplot(311)
        self.format_xaxis(ax1, len(data.cycle_dates))
        if self.config.varno.units is not None:
            ax1.set_ylabel(self.config.varno.units.lower(), fontsize=8)
        plt.plot(data.cycle_dates, data.an_depar)
        plt.plot(data.cycle_dates, data.fg_depar)
        plt.grid(True)
        plt.legend(
            ["an_depar", "fg_depar"],
            loc="upper center",
            ncol=2,
            frameon=False,
            bbox_to_anchor=(0.5, 1.2)
        )
        ax2 = plt.subplot(312)
        self.format_xaxis(ax2, len(data.cycle_dates))
        if self.config.varno.units is not None:
            ax2.set_ylabel(self.config.varno.units.lower(), fontsize=8)
        plt.plot(data.cycle_dates, data.an_depar_std)
        plt.plot(data.cycle_dates, data.fg_depar_std)
        plt.grid(True)
        plt.legend(
            ["an_depar (stdev)", "fg_depar (stdev)"],
            loc="upper center",
            ncol=2,
            frameon=False,
            bbox_to_anchor=(0.5, 1.2)
        )
        ax3 = plt.subplot(313)
        self.format_xaxis(ax3, len(data.cycle_dates))
        ax3.set_ylabel("number", fontsize=8)
        plt.plot(data.cycle_dates, data.obscount)
        plt.grid(True)
        plt.legend(
            ["obscount"],
            loc="upper center",
            ncol=2,
            frameon=False,
            bbox_to_anchor=(0.5, 1.2)
        )
        plt.suptitle(self.get_title())
        plt.savefig(str(self.output_filepath), bbox_inches="tight", dpi=150, pad_inches=0.25)

    @staticmethod
    def format_xaxis(ax, cycle_count):
        ax.yaxis.set_label_position("right")
        for item in ax.get_yticklabels():
            item.set_fontsize(8)
        for item in ax.get_xticklabels():
            item.set_fontsize(8)
        ax.margins(x=0)
        maxticks = cycle_count if cycle_count <= 30 else 30
        locator = mdates.AutoDateLocator(maxticks=maxticks, interval_multiples=False)
        formatter = mdates.ConciseDateFormatter(locator, show_offset=False)
        formatter.formats[3] = "%HZ"
        formatter.zero_formats[3] = "\n%d-%b"
        formatter.zero_formats[2] = "%d\n%b"
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

    def get_vertco_label(self):
        """Get a string representing the vertco type/range"""
        vertco = f'{self.config.vertco_type.label}: '
        vertco += f'{int(self.config.vertco_min)}'
        if self.config.vertco_min != self.config.vertco_max:
            vertco += f' - {int(self.config.vertco_max)}'
        return vertco

    def get_varno_desc(self):
        """Get a string representing the varno description and column if applicable"""
        return self.config.varno.desc

    def get_title(self):
        """Build the title for the chart"""
        title = f'Obs Group: {self.config.obs_group:25}{self.get_vertco_label():>46}\n'
        title += f'{self.get_varno_desc():51}{self.config.cycle1} - {self.config.cycle2}'
        return title
