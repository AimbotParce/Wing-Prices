from timeit import timeit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wings = pd.read_excel("Wings.xlsx", sheet_name="Wings")


MAX = 500
MIN = wings[wings["Chicken Wing Count (w)"] <= MAX].iloc[0]["Chicken Wing Count (w)"]


def predict(knowX, knowY, newX):
    fit = np.polyfit(knowX, np.log(knowY), 1)
    return np.exp(fit[1]) * np.exp(fit[0] * newX)


plt.ion()

timeFig, timeAx = plt.subplots()
timeAx.set_xlim(0, 500)
(timeLine,) = timeAx.plot([], [], "-o")
(predTimeLine,) = timeAx.plot([], [], "-", color="red")

solFig, solAx = plt.subplots()
solAx.set_xlim(0, 500)
(solLine,) = solAx.plot([], [], "-o")
(predSolLine,) = solAx.plot([], [], "-", color="red")

plt.show()


Fullx = np.arange(0, 500)
exes, times, solutionCounts = [], [], []


for i in range(MIN, MAX):
    lower = wings[wings["Chicken Wing Count (w)"] <= i]
    counts = lower["Chicken Wing Count (w)"].values
    prices = lower["Price ($)"].values
    # We want all values of x, y, z, ... such that c1*x + c2*y + c3*z + ... = i and x, y, z, ... are positive integers
    # Naive way: Recursively try out all combinations of x, y, z, ... until we find all solutions that work.
    # Problem: This is extremely slow. In fact, I can predict that this would take about 10^60 years to complete. :(

    solutions = []

    def exploreAllSolutions(current: int, subtractions: list[int] = []) -> list[int]:
        """
        Depth-first search to find the first integer solution to the hyperplane.

        We can't use this algotihm to find all solutions, because it will explore many paths that are not solutions.
        After i=40 or so, it becomes too slow to be useful.
        """
        if current == 0:
            solutions.append(subtractions)
            return  # Don't keep exploring, this is finished
        if current < 0:
            return  # This is not a solution
        # Explore all counts lower than this
        for c in counts[counts <= current]:
            exploreAllSolutions(current - c, subtractions + [c])
        return None

    time = timeit(lambda: exploreAllSolutions(i), number=1)
    # plot
    times.append(time)
    solutionCounts.append(len(solutions))
    exes.append(i)

    timeLine.set_data(exes, times)
    solLine.set_data(exes, solutionCounts)
    pt = predict(exes, times, Fullx)
    ps = predict(exes, solutionCounts, Fullx)
    predTimeLine.set_data(Fullx, pt)
    predSolLine.set_data(Fullx, ps)

    # Set y limits to be from 0 to the maximum value
    timeAx.set_ylim(0, np.max(pt))
    solAx.set_ylim(0, np.max(ps))
    timeAx.autoscale_view()
    solAx.autoscale_view()
    timeFig.canvas.draw()
    solFig.canvas.draw()
    timeFig.canvas.flush_events()
    solFig.canvas.flush_events()

    print(f"{i}) {len(solutions)} solutions found")

    # No need to continue. After around 40 wings, the time it takes to find all solutions starts to become too long.

    # My first idea was to make a meshgrid of all possible values of x, y, z, ... and then brute force it. However,
    # the memory requirements for this are too high.
