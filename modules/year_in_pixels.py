#!/usr/bin/python3
"""Generates a grid with one row for each month and one pixel for each day."""
import calc

def plot(plt, data):
	days = {}
	for d, vs in data.items():
	    days[d] = calc.day_avg(vs)
	calc.plot_days_in_pixels(plt, days)
