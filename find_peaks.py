"""
Script to find and save to csv the locations of data spikes in the MAG data of MESSENGER
"""

import datetime as dt

import hermpy.mag as mag
import hermpy.plotting_tools as hermplot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import scipy.signal
from hermpy.utils import User

# Load entire mission
start = dt.datetime(year=2011, month=3, day=23)
end = dt.datetime(year=2015, month=4, day=30)

full_mission_data = mag.Load_Between_Dates(
    User.DATA_DIRECTORIES["MAG"],
    start,
    end,
    aberrate=False,
    verbose=True,
    multiprocess=True,
    included_columns={
        "date",
        "|B|",
        "X MSM (radii)",
        "Y MSM (radii)",
        "Z MSM (radii)",
    },
)

print("Data Loaded Successfully")

# Find peaks, greater than 10000 nT, with a minimum 1 min between them
peaks, peak_properties = scipy.signal.find_peaks(
    full_mission_data["|B|"], height=10000, distance=60
)

print(len(peaks))

spikes = full_mission_data.iloc[peaks][
    ["date", "X MSM (radii)", "Y MSM (radii)", "Z MSM (radii)"]
]


fig, (xy_axis, xz_axis) = plt.subplots(1, 2)

dates_as_numbers = mdates.date2num(spikes["date"])
norm = mcolors.Normalize(vmin=dates_as_numbers.min(), vmax=dates_as_numbers.max())
cmap = cm.viridis

colors = cmap(norm(dates_as_numbers))

xy_axis.scatter(
    spikes["X MSM (radii)"],
    spikes["Y MSM (radii)"],
    color=colors,
    marker=".",
    zorder=20,
)
xz_axis.scatter(
    spikes["X MSM (radii)"],
    spikes["Z MSM (radii)"],
    color=colors,
    marker=".",
    zorder=20,
)

planes = ["xy", "xz"]
for i, ax in enumerate([xy_axis, xz_axis]):
    hermplot.Plot_Mercury(
        ax, shaded_hemisphere="left", plane=planes[i], frame="MSM"
    )
    hermplot.Add_Labels(ax, planes[i], frame="MSM")
    hermplot.Plot_Magnetospheric_Boundaries(ax, plane=planes[i], add_legend=True)
    hermplot.Square_Axes(ax, 8)

plt.show()
