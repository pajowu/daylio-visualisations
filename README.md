# daylio visualization

This repository contains a collection of scripts that written to visualize the data from [the mood tracker "daylio"](https://daylio.webflow.io/).

All code is written in python3.

## Installation

### Python dependencies

```
pip install -r requirements.txt
```

### Getting the data

The scripts assume that you have an `entries.db` in the current working directory.

### Non-rooted phone

The file can be extracted from an android phone using adb backup by running `export_from_backup.py`.
You need to enable USB Debugging first and authorize your computer with your phone.

### Rooted phone
You can get this file from a rooted phone with

```
adb shell 'su -c "cat /data/data/net.daylio/databases/entries.db"' > entries.db
```

### Simulated data
To run the scripts without actual data, run them with the `--random-data` option.

## Visualisations

### Show all visualizations

To show all visualizations in one plot, simply run

```
./main.py
```

![Example of all visualizations](examples/all.png)

### Mood graph

The mood graph is the classical visualization chosen by daylio.
It simply shows a graph of all the daily averages and colours the parts of the graph in the mood colours.

![Mood graph example](examples/mood_graph.png)

```
./main.py -t mood_graph
```

### Year in pixels

The first visualization is using matplotlib to generate grid with one row for each month and one pixel for each day.
Black pixels are used if the month has less than 31 days.
White pixels are days on which no mood was tracked.
For all other pixels the colour-scheme from daylio is used.

![Example year in pixels](examples/year_in_pixels.png)

```
./main.py -t year_in_pixels
```

### Average calculation

Daylio uses a simple average of all mood values during one day to calculate the mood value of the day.
This has the disadvantage of disproportionately valuing time in which I often track my mood.
These scripts use a different method that is based on the [trapezoidal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule).
The calculation is done on a daily basis, i.e. it does not use the values of other days.

![Difference in mood average using the two methods](examples/average_calculation.png)

```
./main.py -t average_calculation
```

### Entries per day

The power of trapezoidal average calculation and mood tracking in general is stronger the more often the mood is tracked.
`entries_per_day.py` plots the amount of tracked entries per day.

![Plot of the entries per day](examples/entries_per_day.png)

```
./main.py -t entries_per_day
```
