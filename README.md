# daylio visualisation

This repository contains a collection of scritps that I wrote to visualize the data from [my mood tracker daylio](https://daylio.webflow.io/).

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

### Year in pixels

The first visualisation is using matplotlib to generate grid with one row for each month and one pixel for each day.
Black pixels are used if the month has less than 31 days.
White pixels are days on which no mood was tracked.
For all other pixels the colorscheme from daylio is used.

To calculate your year in pixels, run

```
./main.py -t year_in_pixels
```

The output image is saved into `year_in_pixels.png`.

![Example year in pixels](examples/year_in_pixels.png)

### Average calculation

Daylio uses a simple average of all mood values during one day to calculate the mood value of the day.
I find this to be too simple, as it disproportianly counts time in which I often track my mood.
These scripts use a different method that is based on the [trapezoidal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule).
The calculation is done on a daily basis, i.e. it does not use the values of other days.

![Difference in mood average using the two methos](examples/average_calculation.png)

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
