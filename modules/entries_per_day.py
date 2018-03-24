#!/usr/bin/python3
"""Shown how many entries were made per day."""
import datetime


def plot(plt, data):
    days = {}
    for d, vs in data.items():
        days[d] = len(vs)
    x, y = zip(*sorted(days.items(), key=lambda x: x[0]))
    x = [datetime.datetime.fromordinal(i) for i in x]
    plt.plot(x, y, linewidth=1)
