#!/usr/bin/python3
from collections import defaultdict
import sqlite3
import datetime
import calendar
import numpy as np
import random
import sys


def day_avg(vals, style="trapezium"):
	if style == "trapezium":
		if not vals:
			return 0
		if len(vals) == 1:
			return vals[0][1]

		total = 0
		diff = vals[0][0] - vals[-1][0]
		for i in range(1, len(vals)):
			total += ((vals[i][1] + vals[i - 1][1]) / 2) * \
				(vals[i - 1][0] - vals[i][0])
		return total / diff
	else:
		v = [x[1] for x in vals]
		return sum(v) / len(v)


def get_color(mood):
	mood_colors = {5: "#6e7a7c", 4: "#5579a6", 3: "#8f54a5",
	               2: "#42a766", 1: "#fb8c00", 0: "#ff0000"}
	color = mood_colors[round(mood)]
	return tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))


def get_mood_mapping(file):
	groups = {}
	with sqlite3.connect(file) as entrydb:
		c = entrydb.cursor()
		for row in c.execute('SELECT id,mood_group FROM table_moods'):
			groups[row[0]] = row[1]
	return groups


def read_sqlite(file):
	mood_mapping = get_mood_mapping(file)
	data = defaultdict(list)
	with sqlite3.connect(file) as entrydb:
		c = entrydb.cursor()
		for row in c.execute('SELECT date_time,mood FROM table_entries ORDER BY date_time ASC'):
			data[
				datetime.datetime.fromtimestamp(row[0] / 1000).toordinal()
			].append((row[0]/1000, mood_mapping[row[1]]))
	return data


def read_random():
	dates = {}
	for month in calendar.Calendar().yeardatescalendar(datetime.datetime.now().year, width=6)[0]:
		for week in month:
			for date in week:
				random_moods = sorted([
					(datetime.datetime.combine(date,
						datetime.time(random.randint(0, 23),
							random.randint(0, 59),
							random.randint(0, 59))
					).timestamp(), int(5 * random.random()) + 1)
					for i in range(random.randint(0, 5))], key=lambda x: x[0])
				if random_moods and random.random() > 0.2:
					dates[date.toordinal()] = random_moods
	return dates



def month_name(m):
	return calendar.month_name[(m % 12) + 1]


def plot_days_in_pixels(plt, data):
	first_year = datetime.datetime.fromordinal(sorted(data.keys())[0]).year
	last_year = datetime.datetime.fromordinal(sorted(data.keys())[-1]).year

	months = []
	for year in range(first_year, last_year + 1):
		year_data = []
		for month in range(1, 13):
			month_data = [(0, 0, 0)] * 31
			for day in calendar.Calendar().itermonthdates(year, month):
				if day.month == month and day.year == year:
					ordinal = day.toordinal()
					if ordinal in data:
						month_data[day.day - 1] = get_color(data[ordinal])
					else:
						month_data[day.day - 1] = (1, 1, 1)
			year_data.append(month_data)
		months.extend(year_data)

	data = np.array(months)
	mask = data == (1, 1, 1)
	mask2 = data == (0, 0, 0)
	rows = np.flatnonzero(
		(~np.logical_or(mask, mask2)).sum(axis=1).sum(axis=1))

	crop = data[rows.min():rows.max() + 1]
	labels = list(map(month_name, range(rows.min(), rows.max() + 1)))

	plot_months_in_pixels(plt, crop, labels)


def plot_months_in_pixels(plt, data, labels):
	plt.imshow(data)
	plt.yticks(np.arange(len(labels)), labels)
	plt.xticks(np.arange(31, step=2), np.arange(1, 32, step=2))


def frange(start, stop):
	nstart, nstop = start + 0.5, stop + 0.5
	if start == stop:
		return None
	istart = int(nstart)
	istop = int(nstop)

	if istart == istop:
		values = []
	elif start < stop:
		values = list(range(istart, istop + 1))
		values = [x for x in values if start < x - 0.5 < stop]
	else:
		values = list(range(istart, istop - 1, -1))
		values = [x for x in values if start > x - 0.5 > stop]

	return [start] + [x - 0.5 for x in values] + [stop]


def plot_mood_graph(plt, data, **kwargs):
	""" Plot the mood over time, coloring each mood in its color.
	Arguments:
		:data: A list of (timestamp, mood) tuples
	"""
	for i in range(1, len(data)):
		old_mood = data[i - 1]
		new_mood = data[i]
		steps = frange(old_mood[1], new_mood[1])
		if not steps:
			plt.plot([
				datetime.datetime.fromtimestamp(old_mood[0]),
				datetime.datetime.fromtimestamp(new_mood[0])
			], [
				old_mood[1],
				new_mood[1]
			], color=get_color(new_mood[1]), **kwargs)
			continue
		step_time = (old_mood[0] - new_mood[0]) / (old_mood[1] - new_mood[1])
		prev_step = (datetime.datetime.fromtimestamp(old_mood[0]), old_mood[1])
		for step in steps:
			st = datetime.datetime.fromtimestamp(old_mood[0] - (step_time * (old_mood[1] - step)))
			plt.plot([
				prev_step[0],
				st
			], [
				prev_step[1],
				step
			], color=get_color(step / 2 + prev_step[1] / 2), **kwargs)
			prev_step = (st, step)

	plot_mood_axis(plt)


def plot_mood_axis(plt):
	plt.yticks(np.arange(1, 5, 1), ['Rad', 'Good', 'Meh', 'Bad', 'Awful'])
	plt.gca().invert_yaxis()
