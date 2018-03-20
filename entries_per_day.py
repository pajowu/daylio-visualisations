#!/usr/bin/python3
import matplotlib.pyplot as plt
import calc
import datetime


def plot():
    days = {}
    for d, vs in data.items():
        days[d] = len(vs)
    x, y = zip(*sorted(days.items(), key=lambda x: x[0]))
    x = [datetime.datetime.fromordinal(i) for i in x]
    plt.plot(x, y, linewidth=1)


if __name__ == "__main__":
    data = calc.read_data()
    plot()
    plt.tight_layout()
    plt.savefig("entries_per_day.png", dpi=200)
