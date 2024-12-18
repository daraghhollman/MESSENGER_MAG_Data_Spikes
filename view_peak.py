"""
Script to view data spike locations
"""

import datetime as dt

import hermpy.mag as mag
import hermpy.plotting_tools as hermplot
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from hermpy.utils import User

colours = ["#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000"]

# Load entire mission
start = dt.datetime(year=2015, month=1, day=1)
end = dt.datetime(year=2016, month=1, day=1)

full_mission_data = mag.Load_Between_Dates(
    User.DATA_DIRECTORIES["MAG"],
    start,
    end,
    aberrate=False,
    verbose=True,
    included_columns={
        "date",
        "|B|",
        "Bx",
        "By",
        "Bz",
        "range (MSO)",
        "X MSM (radii)",
        "Y MSM (radii)",
        "Z MSM (radii)",
    },
)

print("Data Loaded Successfully")

mag.Remove_Spikes(full_mission_data)

print("Spikes removed")

# Find peaks, greater than 10000 nT, with a minimum 1 min between them
peaks, peak_properties = scipy.signal.find_peaks(
    full_mission_data["|B|"], height=10000, distance=60
)

print(f"# Spikes = {len(peaks)}")

"""
peaks = peaks[np.where(full_mission_data.iloc[peaks]["X MSM (radii)"] > 3)]

if len(peaks) == 0:
    raise RuntimeError("No peaks at this distance")
"""
peaks = peaks[np.where(full_mission_data.iloc[peaks]["Z MSM (radii)"] > -4)]

# shrink data to region around peak
for i in range(len(peaks)):
    query = peaks[i]
    buffer = 120  # seconds
    data = full_mission_data.iloc[query - buffer : query + buffer]

    fig, ax = plt.subplots()

    ax.plot(data["date"], data["|B|"], "o-", color="black", lw=1, label="|B|")
    ax.plot(data["date"], data["Bx"], color=colours[2], lw=0.8, alpha=0.8, label="Bx")
    ax.plot(data["date"], data["By"], color=colours[0], lw=0.8, alpha=0.8, label="By")
    ax.plot(data["date"], data["Bz"], color=colours[-1], lw=0.8, alpha=0.8, label="Bz")

    mag_leg = ax.legend(
        bbox_to_anchor=(0.5, 1.1), loc="center", ncol=4, borderaxespad=0.5
    )

    # set the linewidth of each legend object
    for legobj in mag_leg.legend_handles:
        legobj.set_linewidth(2.0)

    # Format the panels
    ax.set_xmargin(0)
    ax.set_ylabel("Magnetic Field Strength [nT]")
    hermplot.Add_Tick_Ephemeris(ax)

    plt.show()
