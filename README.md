Important Note: The main data file (/data/db_hourly_safe.csv) is missing because of its large size. If this repository becomes frequently used, I will setup GitHub LFS to accomodate it.

# DECO Location Data Processing and Visualization

This repository contains scripts and files which process the location data associated with DECO events. We are able to extract detailed information from DECO users, including the time and GPS coordinates of uploaded events.

We display this information in engaging and interactive ways. Included so far are all-time and monthly leaderboards, displaying the countries most actively contributing to DECO. We are also finding interesting ways of overlaying data on interactive maps, using either Cartopy or the Google Maps API. 

# Instructions

The Python files in /scripts require Python 3.x, as well as the following modules:
- GeoPy (Geolocation client)
- urllib + certifi (web handling for geolocation)
- pylab, numpy (various tools)
- Cartopy + MatPlotLib + mpld3 + Colour (image creation, might be unnecessary in the future as we find better tools)
- gmplot (Google Maps API, might also be replaced)

I was able to install all of these locally with Pip, although at one time there were problems getting Cartopy to work without manual installation.

The file /data/db_hourly_safe.csv needs to be regularly fetched from /net/deco on Cobalt, after which the scripts are executed. 

## Scripts and Accessory Files

We use the GeoPy client for Python to parse location data. It associates detailed location data (i.e. Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...) to latitude and longitude coordinates.

In order to cut down on the number of geolocator requests we have to make for the large volume of DECO data, we 'bin' nearby locations. In other words, we submit only one geolocator request for an event in a not-seen-before location, and from then on any events found to be near this location (~0.1 degrees latitude/longitude) do not need to have their locations fetched. This works because we care most about identifying states and countries, which usually span more than 0.1 degrees. 

All of this processing is handled by locationProcessing.py located in /scripts/

HTML files are created from the csv files kept up to date by locationProcessing.py, and are handled by htmlGenerator.py (also in /scripts/)


## Authors and Acknowledgments

TODO
