#!/usr/bin/python3
"""Generates a grid with one row for each month and one pixel for each day."""
import calc
import datetime

def plot(plt, data):
	days = {}
	for d, vs in data.items():
	    days[d] = calc.day_avg(vs)
	days = sorted([(datetime.datetime.fromordinal(x).timestamp(),y) for x,y in days.items()], key=lambda x: x[0])
	calc.plot_mood_graph(plt, days, linewidth=5)
