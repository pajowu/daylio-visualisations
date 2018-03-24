#!/usr/bin/python3
import matplotlib.pyplot as plt
import calc
import datetime


def plot(style):
	if style == "raw":
		x = []
		y = []
		for i in data:
			for j in data[i]:
				x.append(datetime.datetime.fromtimestamp(j[0]/1000))
				y.append(j[1])
	else:
		days = {}
		for d, vs in data.items():
			days[d] = calc.day_avg(vs, style)
		x, y = zip(*sorted(days.items(), key=lambda x: x[0]))
		x = [datetime.datetime.fromordinal(i) for i in x]
	plt.plot(x, y, label=style)


if __name__ == "__main__":
    data = calc.read_data()
    plot("raw")
    plot("trapezium")
    plot("old")
    legend = plt.legend()
    plt.tight_layout()
    plt.savefig("average_calculation.png", dpi=200)
