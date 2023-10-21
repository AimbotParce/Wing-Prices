from timeit import timeit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wings = pd.read_excel("Wings.xlsx", sheet_name="Wings")

MAX = 500
MIN = int(wings[wings["Chicken Wing Count (w)"] <= MAX].iloc[0]["Chicken Wing Count (w)"])
# Let's choose the dtype for the meshgrids so that we can store the biggest possible value
# This biggest value will be buying the minimum pack to make up to MAX wings:
maxSize = MAX // MIN
meshgridDtype = np.min_scalar_type(maxSize)

for i in range(MIN, MAX):
    lower = wings[wings["Chicken Wing Count (w)"] <= i]
    counts = lower["Chicken Wing Count (w)"].values
    prices = lower["Price ($)"].values
    # We want all values of x, y, z, ... such that c1*x + c2*y + c3*z + ... = i and x, y, z, ... are positive integers

    # Let's try again the mesgrid idea, but lets be smart about it, instead of initializing all arrays at once with a size
    # too large, lets set the size of each dimension to be at most the number of times that pack should be buyed to get
    # to i (rounding down).

    dimensions = [np.arange(0, i // c, dtype=meshgridDtype) for c in counts]
    space = np.meshgrid(*dimensions)

    size = sum([space[i].size for i in range(len(space))])
    mem = size * space[0].itemsize / 1024 / 1024  # in MB

    print(f"{i}) Will take {mem:.2f} MB of memory for {size} elements")

    if mem > 9000:  # 8 GB
        print("ERROR: Stoping because it will take too much memory")
        quit()
