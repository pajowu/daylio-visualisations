#!/usr/bin/python3
"""Compares two ways of calculating the daily mood average."""
import calc
import datetime


def plot_average(plt, data, style):
    days = {}
    for d, vs in data.items():
        days[d] = calc.day_avg(vs, style)
    x, y = zip(*sorted(days.items(), key=lambda x: x[0]))
    x = [datetime.datetime.fromordinal(i) for i in x]
    plt.plot(x, y, label=style)


def plot(plt, data):
    for style in ["trapezium", "mean"]:
        plot_average(plt, data, style)
    plt.legend()
