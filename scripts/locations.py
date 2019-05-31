#######################################################
## Processes location data associated with DECO events
## Author: Blake Gallay
#######################################################
import geopy
import argparse
import csv
import datetime
import json
from geopy.geocoders import OpenCage
import math

import numpy as np

# Dictionary for interpreting US state abbreviations
state_abbreviations = {'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas',
					   'CA':'California','CO':'Colorado','CT':'Connecticut',
					   'DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii',
					   'ID':"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
					   'KS':"Kansas",'KY':"Kentucky",'LA':'Louisiana','ME':'Maine',
					   'MD':'Maryland','MA':'Massachusetts','MI':'Michigan',
					   'MN':'Minnesota',"MS":'Mississippi','MO':'Missouri',
					   'MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire'
					   ,'NJ':'New Jersey','NM':'New Mexico','NY':'New York',
					   'NC':'North Carolina','ND':'North Dakota','OH':'Ohio',
					   'OK':'Oklahoma','OR':"Oregon",'PA':'Pennsylvania',
					   'RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota',
					   'TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont',
					   'VA':'Virginia','WA':'Washington','WV':'West Virginia',
					   'WI':'Wisconsin','WY':'Wyoming'}

# Import the geolocator and use an API key
## Limitations: 2500/day, 1/second
geolocator = OpenCage("e1b89ffd560a4b39b9d856904798fc7b")
#78e7d0d08860206c27e848a7bc4f1451 66ffcb477c3548c99085d0cf5e87954e KEYS
# e1b89ffd560a4b39b9d856904798fc7b NEW KEY

# Radius of location bins (in latitude/longitude degrees)
bin_size = 1

# Filepaths
main_data_path = '../data/db_hourly_safe.csv'
event_locations_path = '../data/event_locations.csv'
lastID_path = '../data/lastID.csv'
userLocations_path = '../data/userLocations.csv'
binnedLocations_path = '../data/binnedLocations.csv'
contributingCountries_path = '../data/contributingCountries.csv'
states_path = '../data/states.csv'
topofmonth_path = '../data/topOfMonth.csv'
topcountries_path = '../data/topCountries.csv'
newcountry_path = '../data/newCountries.csv'


# Takes CSV file path, returns NumPy array
def import_csv(path, headers=False):
	temp = []
	with open(path) as file:
		reader = csv.reader(file)
		for row in reader:
			if(not headers):
				temp.append(row)
			headers = False
	out = np.array(temp)
	return out
	
# Writes NumPy array to CSV file
def write_csv(data, path, headers=[]):
	temp = []
	with open(path, "w") as file:
		writer = csv.writer(file)
		if headers != []:
			writer.writerow(headers)
		for item in data:
			try:
				writer.writerow(item)
			except UnicodeEncodeError:
				continue

# Indices of main DECO csv 
class Index:
	time = 2
	ID = 11
	latitude = 12
	longitude = 13
	deviceID = 15
	classification = 21
	country = 22

# ID of most recent event previously processed
# i.e. 510525150
lastID = int(import_csv(lastID_path)[0])

# All DECO event IDs and their corresponding countries
event_data = import_csv(event_locations_path, True)
event_locations = {}
for event in event_data:
	if(len(event) > 1):
		event_locations[event[0]] = [event[1], event[2]]

# Locations of all DECO users
Users = import_csv(userLocations_path, True)

# Latitude/Longitude Coordinate Bins
Coordinates = import_csv(binnedLocations_path, True)

# Importing list of contributing countries + states :

# Total event count from each country
# Country Name : # Of Events
Countries = {} 

# All country data from ContributingCountries.csv
CountryData = import_csv(contributingCountries_path, True)

for item in CountryData:
	Countries[item[0]] = [int(item[1]), int(item[3])]
	
# Same process w/ US states
States = {}
StateData = import_csv(states_path, True)
for item in StateData:
	if(item[1] != "50"):
		States[item[0]] = int(item[1])
	
def main():
	global Coordinates
	global Users
	global lastID
	current_time = datetime.datetime.now()
	
	# All data from db_hourly_safe.csv
	data = import_csv(main_data_path, True)

	# Events which are being processed for the first time, 
	# and are from a new location
	data_toGeolocate = []
	userdict = {}
	
	for user in Users:
		userdict[user[0]] = user[1]
		
	
	# All events from the past month
	monthEvents = []

	for event in data:
	
		classification = event[Index.classification]
		classified = (classification != "" and classification != "unclassified")
	
		loc = check_bins(event, Coordinates)
		
		if(loc != None):
			userid = event[Index.deviceID]
			if userid not in userdict:
				userdict[userid] = loc[0]
		
		if(filter(event)):
			event_ID = int(event[Index.ID])
			
			# Only process 'new events', indicated by an ID greater than 
			# the last one previously processed.
			
			if(event_ID > lastID):

				# Check if the associated device has been cataloged
				newUser = True
				
				user_id = event[Index.deviceID]
				
				newUser = user_id in userdict

				location = check_bins(event, Coordinates)
				
				if(location == None):
					data_toGeolocate.append(event)
				else:
					event_country = location[0]
					event_state = location[1]
				
					# Add to the country count
					for country in Countries:
						if(country == event_country):
							Countries[country][0] += 1
							if(classified):
								Countries[country][1] += 1
					# If from a US state, add to the state count
					if event_state in state_abbreviations:
						state_name = state_abbreviations[event_state]
						for state in States:
							if(state == state_name):
								States[state_name] += 1
					# If a new user, add to the list
					if(newUser):
						userdict[user_id] = event_country
						
					event_locations[event_ID] = [event_country, event_state]
					
			# Finds events which occurred within the past month
			event_time = datetime.datetime.strptime(event[Index.time], '%Y-%m-%d %H:%M:%S.%f')
			if(current_time - event_time).total_seconds() < 26280000:
				monthEvents.append(event)
		
	# Turn lists into numpy arrays
	data_toGeolocate = np.array(data_toGeolocate)
	monthEvents = np.array(monthEvents)
	
	# To tell which events are 'new' on each run, we keep track of the latest eventID processed.
	lastID = [[event_ID]]
	write_csv(lastID, lastID_path)
	
	for event in data_toGeolocate:
	
		classification = event[Index.classification]
		classified = (classification != "" and classification != "unclassified")
	
		time = event[Index.time]
		id = int(event[Index.ID])
		lat = float(event[Index.latitude])
		long = float(event[Index.longitude])

		event_country = ""
		
		# Don't bother with nonsense coordinates
		if(( lat == 0 and long == 0) or math.fabs(lat) > 1000 or math.fabs(long) > 1000):
			continue
		
		# Check if the location lies within a newly-cataloged bin
		location_check = check_bins(event, Coordinates, True)

		if(location_check != None):
			event_country = location_check[0]
			event_state = location_check[1]
			event_coords = location_check[2]
		else:
			# Use the OpenCage geolocator to convert coordinates into addresses,
			# Ignores nonsense coordinate i.e. (0,0)
			# Makes multiple attempts in the case of a timeout.
			
			event_coords = [lat, long]
			
			found = False
			max_attempts = 5
			attempts = 0
			new = False
			while not found and attempts < max_attempts:
				try:
					location = geolocator.reverse([lat, long])
					print(lat)
					print(long)
					print('new location')
					new = True
					found = True
				except geopy.exc.GeocoderTimedOut:
					attempts += 1
					location = None
			
			if(location == None or location == ""):
				Coordinates = np.append(Coordinates, [[lat, long, "None", "None"]], axis=0)
				continue
			
			address = location[0].address
				
			if(address == 'Null Island' or address == 0 or location == None):
				Coordinates = np.append(Coordinates, [[lat, long, "None", "None"]], axis=0)
				continue
			
			address_data = address.split(", ")
			
			event_country = address_data[-1]
			
			# The following code tries to account for different address
			# formats and missing data, but some countries and states might
			# still be going by undetected.
			try:
				event_state = address_data[-2].split(" ")[0]
				if event_state in state_abbreviations:
					for State in States:
						if State[0] == state_abbreviations[event_state]:
							event_state = State[0]
			except IndexError:
				event_state = None
				
			try:
				extended_state_info = address_data[-2].encode('utf-8')
			except IndexError:
				Coordinates = np.append(Coordinates, [[lat, long, event_country, event_state]], axis=0)
				continue
				
			try:
				info = extended_state_info.decode().split(" ")
			except UnicodeDecodeError:
				Coordinates = np.append(Coordinates, [[lat, long, event_country, event_state]], axis=0)
				continue
			
			try:
				try:
					float(event_country)
					
					if(len(info) > 1):
						event_country = str(info[0] + " " + info[1])
					else:
						country = str(info[0])
							
					event_state = address_data[-3]
						
				except ValueError:
					if(len(info) > 1):
						event_state = str(info[-2])
					elif(len(info) == 1):
						event_state = str(info[0])
					else:
						state = None					
			except IndexError:
				Coordinates = np.append(Coordinates, [[lat, long, event_country, event_state]], axis=0)
				continue
				
			Coordinates = np.append(Coordinates, [[lat, long, event_country, event_state]], axis=0)

		# Add to counts
		if event_country in Countries:
			Countries[event_country][0] += 1
			if(classified):
				Countries[event_country][1] += 1

		if event_state in States:
			States[event_state] += 1
			
		if event_state in state_abbreviations:
			States[state_abbreviations[event_state]] += 1
				
		# If a new user, add to the user list
		user_id = event[15]
		if user_id not in userdict:
			userdict[user_id] = event_country
			
		event_locations[id] = [event_country, event_state]

	userlist = []
	for user in userdict:
		userlist.append([user, userdict[user]])
	Users = np.array(userlist)
	
	# Catalog the number of users per country
	# Really quick and bad implementation
	# TODO: optimize
	countries_usercount = {}
	for country in Countries:
		countries_usercount[country] = 0
	for user in Users:
		try:
			countries_usercount[user[1]] += 1
		except KeyError:
			pass
	
	# Write data to files
	countrieslist = []
	for country in Countries:
		countrieslist.append([country, Countries[country][0], countries_usercount[country], Countries[country][1]])
		print(Countries[country][1])
		
	stateslist = []
	for state in States:
		stateslist.append([state, States[state]])
		
	write_csv(countrieslist, contributingCountries_path, ["Country", "Event Count", "Users", "Classified Events"])
	
	write_csv(stateslist, states_path, ["State", "Event Count"])

	write_csv(Coordinates, binnedLocations_path, ["Latitude", "Longitude", "Country", "State"])
	
	write_csv(Users, userLocations_path, ["DeviceID", "Country"])
	
	# Turn dictionary into comprehensible list
	eventslist = []
	for event in event_locations:
		location = event_locations[event]
		eventslist.append([event, location[0], location[1]])
	
	write_csv(eventslist, event_locations_path, ["Event ID", "Country"])
	
	lists(Countries, States, monthEvents)
				
# === Location Binning ===
# We keep a catalog of known locations, in order to minimize daily geolocator requests.
# We compare the latitude/longitude coordinates of a new event to this catalog.
# 	- If it is nearby a known coordinate, we do not use the geolocator, 
#		and instead use the cataloged location
#	- If it is in a new place, we fetch its location using the geolocator, 
#		and add its location to the catalog
def check_bins(event, coords, get_coord=False):
	
	lat = float(event[Index.latitude])
	long = float(event[Index.longitude])
	
	# Iterate through all of the cataloged location coordinates
	for coordinate in coords:
		if(len(coordinate) == 0):
			continue
		clat = float(coordinate[0])
		clong = float(coordinate[1])
				
		coord_country = coordinate[2]
		
		coord_state = coordinate[3]
				
		# Check if the event's coords are close to a cataloged location
		if (
			lat > clat - bin_size and
			lat < clat + bin_size and
			long > clong - bin_size and
			long < clong + bin_size
			):
				if(get_coord):
					return [coord_country, coord_state, coordinate]
				else:
					return [coord_country, coord_state]
		
	return None
	
# When reading an event row in the main data csv
# Perform a number of checks/filters 
# Returns True if the event passes all filters
def filter(event):

	# Make sure no column headers are being read
	if(event[Index.latitude] == "latitude"):
		return False
		
	# Make sure the row is full
	if(len(event) < 11):
		return False
		
	# Events from phones with broken clocks
	# This might not be necessary, removed for now
	#aq_time = datetime.datetime.strptime(event[Index.time], '%Y-%m-%d %H:%M:%S.%f') 
	#if((current_time - aq_time).total_seconds() > 230000000):
	#	return False
		
	return True

# Generates spreadsheets that display the top contributor countries
# topCountries.csv (all time) and topOfMonth.csv 
def lists(countries, states, monthEvents):
	
	# Find top contributing countries of the month, create monthly leaderboard
	monthCountries = {}
	for event in monthEvents:
		id = event[Index.ID]
		if id in event_locations:
			country = event_locations[id][0]
			if country in Countries:
				if country in monthCountries:
					monthCountries[country] += 1
				else:
					monthCountries[country] = 1
	monthList = []
	for country in monthCountries:
		monthList.append([monthCountries[country], country])
		
	monthList = sorted(monthList, reverse=True)
	
	write_csv(monthList, topofmonth_path)
	
	# Sort countries by number of events, create leaderboard file
	sorted_countries = []
	for country in Countries:
		sorted_countries.append([Countries[country][0], country])
	sorted_countries = sorted(sorted_countries, reverse=True)
	
	write_csv(sorted_countries, topcountries_path)

if __name__ == "__main__":
	main()