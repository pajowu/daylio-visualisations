# daylio visualisation

This repository contains a collection of scritps that I wrote to visualize the data from [my mood tracker daylio](https://daylio.webflow.io/).

All code is written in python3.

## Installation

### Python dependencies

```
pip install -r requirements.txt
```

### Getting the data

Currently the scripts assume that you have an `entries.db` in the current working directory. You can get this file from a rooted phone with

```
adb shell 'su -c "cat /data/data/net.daylio/databases/entries.db"' > entries.db
```

To run the scripts with actual data, run them with the `--random-data` option.

## Visualisations

### Year in pixels

The first visualisation is using matplotlib to generate grid with one row for each month and one pixel for each day.
Black pixels are used if the month has less than 31 days.
White pixels are days on which no mood was tracked.
For all other pixels the colorscheme from daylio is used.

![Example year in pixels](year_in_pixels.png)
