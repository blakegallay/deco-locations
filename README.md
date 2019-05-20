important note: the main data file (/data/db_hourly_safe.csv) is missing because of its large size. if this repository becomes frequently used, I will setup GitHub LFS

# DECO Location Data Processing and Visualization

This repository contains scripts and files which process the location data associated with DECO events. We are able to extract detailed information from DECO users, including the time and GPS coordinates of uploaded events.

We display this information in engaging and interactive ways. Included so far are all-time and monthly leaderboards, displaying the countries most actively contributing to DECO. We are also finding interesting ways of overlaying data on interactive maps, using either Cartopy or the Google Maps API. 

## Scripts and Accessory Files

We use the GeoPy client for Python to parse location data. It associates detailed location data (i.e. Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...) to latitude and longitude coordinates.

In order to cut down on the number of geolocator requests we have to make for the large volume of DECO data, we 'bin' nearby locations. In other words, we submit only one geolocator request for an event in a not-seen-before location, and from then on any events found to be near this location (~0.1 degrees latitude/longitude) do not need to have their locations fetched. This works because we care most about identifying states and countries, which usually span more than 0.1 degrees. 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Authors and Acknowledgments


