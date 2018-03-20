#!/usr/bin/python3
import calc

if __name__ == "__main__":
	data = calc.read_data()
	days = {}
	for d, vs in data.items():
	    days[d] = calc.day_avg(vs)
	calc.plot_days(days, out_file="year_in_pixels.png")
