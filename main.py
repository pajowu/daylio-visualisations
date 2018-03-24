#!/usr/bin/python3
import argparse
import importlib
import textwrap
from matplotlib import pyplot
import calc

VIZS = ["year_in_pixels", "average_calculation", "entries_per_day", "mood_graph"]


def load_viz(viz, mod_dir="modules"):
	return importlib.import_module("." + viz, "modules")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='daylio visualizations.')
	parser.add_argument('-t', '--type', dest='viz_type',
	                    default="year_in_pixels",
	                    help=('What visualizations type shall be run. '
	                          'For a list of available ones use `--type LIST`'))

	parser.add_argument('--random-data', action="store_true")

	args = parser.parse_args()

	if args.viz_type == "LIST":
		for viz in VIZS:
			module = load_viz(viz)
			print("{}: ".format(viz))
			docstring = "No documentation given"
			if module.__doc__:
				docstring = module.__doc__
			print(textwrap.fill(docstring, initial_indent="    ", subsequent_indent="    "))
	else:
		module = load_viz(args.viz_type)
		data = calc.read_data()
		module.plot(pyplot, data)
		pyplot.show()
