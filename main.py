#!/usr/bin/python3
import argparse
import importlib
import textwrap
from matplotlib import pyplot
import calc
import math

VIZS = ["year_in_pixels", "average_calculation", "entries_per_day", "mood_graph"]


def load_viz(viz, mod_dir="modules"):
	return importlib.import_module("." + viz, "modules")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='daylio visualizations',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t', '--type', dest='viz_type',
	                    default="ALL",
	                    help=('What visualizations type shall be run as a comma seperated list. '
	                          'For a list of available ones use `--type LIST`. By default all plots '
	                          'are shown'))

	parser.add_argument('--random-data', action="store_true", help=("If this option is specified, "
		"the mood data will be generated randomly instead of reading the entries.db"))

	parser.add_argument('-s', '--sqlite-file', help="Sqlite file to read the mood tracking data from",
		default="entries.db")

	parser.add_argument('-o', '--output', help="File to write the generated plot(s) to")

	args = parser.parse_args()

	viz_to_run = args.viz_type.split(",")
	if viz_to_run == ["ALL"]: viz_to_run = VIZS

	if args.viz_type == ["LIST"]:
		for viz in VIZS:
			module = load_viz(viz)
			docstring = "No documentation given"
			if module.__doc__:
				docstring = module.__doc__
			print(textwrap.fill("{}: {}".format(viz, docstring),
				initial_indent="", subsequent_indent="    "))

	elif set(viz_to_run) - set(VIZS) == set():
		px = math.sqrt(len(viz_to_run))
		py = math.ceil(len(viz_to_run) / px)
		pyplot.figure(figsize=(6.4*px, 4.8*py))
		if args.random_data:
			data = calc.read_random()
		else:
			data = calc.read_sqlite(args.sqlite_file)
		for pi,viz in enumerate(viz_to_run):
			pyplot.subplot(px,py,pi+1)
			module = load_viz(viz)
			module.plot(pyplot, data)
			pyplot.title(" ".join(viz.split("_")).title())
		if args.output:
			pyplot.tight_layout()

			pyplot.savefig(args.output, dpi=300)
		else:
			pyplot.show()

	else:
		print("Invalid visualization(s) specified: {}".format(set(viz_to_run) - set(VIZS)))
