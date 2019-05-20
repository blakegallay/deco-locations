#!/usr/bin/env python

##===========================================================================##
## Extracts location information from DECO events and creates spreadsheets
## containing statistics on countries, states, etc. New data is appended to
## existing spreadsheets to keep them up-to-date.
##===========================================================================##

import geopy
import argparse
import csv
import datetime
import json
from geopy.geocoders import OpenCage

if __name__ == "__main__":
	
	# CSV File containing list of all DECO event ID's and countries of origin
	ids_countries = {}
	try:
		with open('../data/ids_countries.json') as data_file:	
			ids_countries = json.load(data_file)
	except FileNotFoundError:
		pass

	# Import the geolocator program and use an API key
	## Limitations: 2500/day, 1/second
	geolocator = OpenCage("78e7d0d08860206c27e848a7bc4f1451")
	#78e7d0d08860206c27e848a7bc4f1451 66ffcb477c3548c99085d0cf5e87954e KEYS

	# The last indexed event ID - used to determine 'new'/'old' data
	with open('../data/lastID.csv') as l:
		reader = csv.reader(l)
		for row in reader:
			lastID = row[0]
   
	with open("../data/db_hourly_safe.csv") as f:
		csv_f = csv.reader(f)
		dataTable = []
		coordinates = []
		newEvents = []
		fullTable = []
		weekEvents = []
		withinEvents = []
		cTime = datetime.datetime.now()
		u = 0
		with open('../data/binnedLocations.csv') as gridcoords: # List of binned latlon coordinates
			reader = csv.reader(gridcoords)
			for coordinate in reader:
				coordinates.append(coordinate)
		for row in csv_f:
			if(len(row) > 11):
				if(row[12] != "latitude"): # Makes sure that the top row (column headers) isn't being read
					eventTime = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f') # Gets current time
					if(int(row[11]) > int(lastID)):
						fullTable += [row]
						
						#if((cTime - eventTime).total_seconds() < 1000000000):
						if(True):
							with open('../data/binnedCoordinates.csv') as cds:
								coordsreader = csv.reader(cds)
								new = True
								for coordinate in coordsreader:
									if(len(coordinate)>0):
										# First level of binning - determines if event coordinates are within 0.1 degrees of an indexed grid point
										if(float(row[12]) > float(coordinate[0]) - 1 and float(row[12]) < float(coordinate[0]) + 1 and float(row[13]) < float(coordinate[1]) + 1 and float(row[13]) > float(coordinate[1]) - 1):
											new = False
											with open('../data/binnedLocations.csv') as locations:
												reader2 = csv.reader(locations)
												 
												for r in reader2:
													if(len(r)!=0):
														if(r[0] == row[12] and r[1] == row[13]):
															nextCountry = r[2]
															withinEvents += [nextCountry]
								if(new == True):
									dataTable += [row] 
							u += 1
					if((cTime - eventTime).total_seconds() < 2628000): # Finds events which occurred within the past week
						weekEvents.append(row)
					ID = row[11]
	lastID = ID
	with open('../data/lastID.csv', 'w') as last: # Re-writes lastID
		writer = csv.writer(last)
		writer.writerow([lastID])
		
	with open("../data/contributingCountries.csv") as y: # List of DECO contributor countries
		csv_y = csv.reader(y)
		countryTable = []
		for row in csv_y:
			countryTable += [row]
	states = []
	with open('../data/states.csv') as st: # US states
		streader = csv.reader(st)
		r = 0
		for row in streader:
			if(r != 0):
				states += [row]
			r = 1
	r = 1
	outTable = []
	countries = []
	magnitude = {}
	u = 0
	for j in countryTable:
		countries.append(j)
		magnitude[j[0]] = [u,int(j[1])]
		u += 1

	altitudes = {} # not implemented - future goal?
	m = 0
	coords = [[] for n in range(0)]
	rt = 0
	topOfWeek = []
	gridpoints = 0
	
	weekCountries = []
 
	newCountries = []
	for event in withinEvents: # Goes through events which were close to cataloged grid points
		
		for cntry in countries:
			if(cntry[0] == event[0]):
				cntry[0][1] += 1
	#print(countries)
	for row in dataTable: # Goes through all events which made it through filters
		rt += 1
		 
		v = 0
	  # Extract info from the csv file
		date = row[2]
		eventID = row[11]
		latlon = (row[12], row[13])
		cont = True
		if(float(latlon[0]) == 0 and float(latlon[1]) == 0 or float(latlon[0]) > 1000 or float(latlon[1]) > 1000):
			continue
		for u in range(len(coords)):
			
			if(float(latlon[0]) < float(coords[u][0]) + 1 and float(latlon[0]) > float(coords[u][0]) - 1 and float(latlon[1]) < float(coords[u][1]) + 1 and float(latlon[1]) > float(coords[u][1]) - 1):
				cont = False		
				v = u  
				break
			
		if(cont == True):
			
			coords.append([latlon[0],latlon[1],0])
			#print(len(coords))  
		if(len(coords) == 0):
			coords.append([latlon[0],latlon[1],0])
			
		# Uses the geopy geolocator to convert coordinates into addresses,
		# ignores points in the middle of nowhere
		# makes multiple attempts in the case of a timeout
		found = False
		attempt = 0
		nattempts = 5
		#print(rt)
		if(cont == True):
			print(len(coords))
			while not found and attempt < nattempts:
				try:
					location = geolocator.reverse(latlon)
					found = True
				except geopy.exc.GeocoderTimedOut:
					attempt += 1
					print('Geocoder timed out %i times...')
					location = None
			
			if location == None:
				continue
			else:
				address = location[0].address
			
			coords[-1][2] = address
			if address == 'Null Island' or address == 0:
				continue
			print(address)
		else:
			if location == None:
				continue
			address = coords[v][2]
		   
		if address == 'Null Island' or address == 0:
				continue
		if location == None:
				continue
		# Selects country and state from long address
		## NOTE: not all of the addresses are in the same order
		## this needs to be changed
		#print(address)
		addresslist = address.split(", ")
		#country = addresslist[-1].encode('utf-8')
		
		
		cs = False
		country = addresslist[-1]
		print(country)
		if row in weekEvents:
			pass
		
		
		state_abbreviations = {'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",'KS':"Kansas",'KY':"Kentucky",'LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota',"MS":'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':"Oregon",'PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'}
		
		try:
			state = addresslist[-2].split(" ")[0]
		except IndexError:
			continue
		full_state_string = state
		if state in state_abbreviations:
			instates = False
			for index in range(len(states)):
				if(states[index][0] == state_abbreviations[state]):
					instates = True
					states[index][1] = int(states[index][1]) + 1
			if(instates == False):
				states.append([state_abbreviations[state], 1])
			full_state_string = state_abbreviations[state]
		
		try:
			float(country)
			cs = True
		except ValueError:
			cs = False
		try:
			stateinfo = addresslist[-2].encode('utf-8')
		except IndexError:
			continue
		stateinfo = stateinfo.decode().split(" ")
		
		
		
		
		try:
			if(cs == True):
				if(len(stateinfo) > 1):
					country = str(stateinfo[0] + " " + stateinfo[1])
				else:
					country = str(stateinfo[0])
				state = addresslist[-3]
			else:
			
				if len(stateinfo) == 2:
					state = str(stateinfo[-2])
				if len(stateinfo) == 1:
					state = stateinfo[0]
				else:
					state = "null"
					
		except IndexError:
			continue
		notIndexed = True
		for n in range(len(countries)):
			if(countries[n][0] == country):
				notIndexed = False
				
		if(cont == True):
			coordinates.append([row[12],row[13],country])
		if(notIndexed == True):
			#altitudes[country] = []
			countries.append([country, 0])
			magnitude[country] = [m, 1]
			countries[magnitude[country][0]][1] = magnitude[country][1]
			countries[magnitude[country][0]] += [magnitude[country][1] / r]
			m += 1
			for n in countries:
				if(n[0] == country):
					if(n[1] == '0' or n[1] == 0):
						newCountries += [country]
		else:
			#altitudes[country] += [row[3]]
			magnitude[country][1] += 1
			
		outTable.append([eventID, latlon, country, state, date])
		countries[magnitude[country][0]][1] = magnitude[country][1]
		#countries[magnitude[country][0]][2] = (magnitude[country][1]) / r
		if(r > 800000000000):
			break
		ids_countries[row[11]] = country
		
		r += 1
		

	#AvgAltitude = [[] for l in range(0)]
	#totalAltitude = 0
	
	#for n in altitudes:
	 #   totalAltitude = 0
	  #  for x in altitudes[n]:
	  #	  if(x != "0"):
	  #		  totalAltitude += float(x)
	 #   newAltlist = []
	#	newAltlist += [n]
	#	newAltlist += [totalAltitude/ len(altitudes[n])]
	#	AvgAltitude.append(newAltlist)
		
	print(gridpoints)
	#print(countries)
	print("got to creation of csv files")
	weekCoords = []
	
			
	print("making weekCoords....")
	for wEvent in weekEvents:
		latlon = [wEvent[12],wEvent[13]]
		cont = True
		if(float(latlon[0]) == 0 and float(latlon[1]) == 0 or float(latlon[0]) > 1000 or float(latlon[1]) > 1000):
		   
			continue
		for u in range(len(weekCoords)):
			
			if(float(latlon[0]) < float(weekCoords[u][0]) + 5 and float(latlon[0]) > float(weekCoords[u][0]) - 5 and float(latlon[1]) < float(weekCoords[u][1]) + 5 and float(latlon[1]) > float(weekCoords[u][1]) - 5):
				
				
				for t in range(len(weekCoords)):
					if(weekCoords[t][0] == latlon[0] and weekCoords[t][1] == latlon[1]):
						weekCoords[t][2] += 1
				cont = False
				v = u  
				break
			
		if(cont == True):
			
			weekCoords.append([latlon[0],latlon[1],0])
			#print("new coord found")
			
			
	print("making countries...")
	for wCoord in weekCoords:
		countryIndexed = False
		country = (((geolocator.reverse([wCoord[0],wCoord[1]]))[0].address).split(", "))[-1]
		print(country)
		for n in range(len(weekCountries)):
			if(country == weekCountries[n][1]):
				countryIndexed = True
		if(countryIndexed == False):
			weekCountries.append([wCoord[2], country])
		else:
			for u in range(len(weekCountries)):
				if(weekCountries[u][1] == country):
					weekCountries[u][0] += wCoord[2]
	
	# Starts a new csv file
	#outFile = 'opencage2_%i_%i.csv' % (args.start, args.stop)
	#with open(outFile, "w") as f:
		 #Writes the desired information into the new csv file
	 #   my_writer = csv.writer(f)
	 #   for row in outTable:
	 #	   try:
	 #		   my_writer.writerow(row)
	 #	   except UnicodeEncodeError:
	 #		   continue
	 #	   pass
	print("making binnedCoordinates.csv")
	with open('../data/binnedLocations.csv', "w") as gcoords:
		writ = csv.writer(gcoords)
		for nextCoord in coordinates: 
			writ.writerow(nextCoord)
				
	with open('../data/binnedCoordinates.csv','w') as gridcoords:
		writer = csv.writer(gridcoords)
		for coord in coordinates:
			if(len(coord)!=0):
				writer.writerow([coord[0],coord[1]])
	print("making old")
	
	reversed_countries = []
	
	for country in countries:
		reversed_countries.append([int(country[1]),country[0]])
	sorted_countries = sorted(reversed_countries, reverse=True)
	
	print("makine top of all time csv...")
	all_file = '../data/topCountries.csv'
	with open(all_file, "w") as a:
		awr = csv.writer(a)
		for sc in sorted_countries:
			print(sc)
			if sc[1] == "":
				continue
			try:
				for country in countries:
					if sc[1] == country[0]:
						awr.writerow(sc)
			except UnicodeEncodeError:
				continue
			pass
			
	print('making countries.csv')
	outfile2 = '../data/contributingCountries.csv'
	with open(outfile2, "w") as g:
		n = 0
		mw2 = csv.writer(g)
		for r in countries:
			if(n < 197):
				try:
					r[2] = float(r[1])/float(r[3])
					mw2.writerow(r)
				except UnicodeEncodeError:
					continue
				pass
			n += 1
		#mw2.writerow(top)
	print('sorting')
	weekCountriesSorted = sorted(weekCountries, reverse=True)
	print('making topofweek')
	outfile3 = '../data/topOfWeek.csv'
	with open(outfile3, "w") as t:
		mw3 = csv.writer(t)
		for wc in weekCountriesSorted:
			try:
				for country in countries:
					if wc[1] == country[0]:
						mw3.writerow(wc)
			except UnicodeEncodeError:
				continue
			pass
	if(len(newCountries) != 0):
		for j in newCountries:
				for n in countries:
					if(n[0] == j):
						if(n[1] != '0' and n[1] != 0):
							with open('newCountries.csv', "w") as new:
								nw = csv.writer(new)
								nw.writerow([j])
			
	statescsv = '../data/states.csv'
	with open(statescsv, 'w') as s:
		sw = csv.writer(s)
		sw.writerow([len(states),50])
		for state in states:
			try:
				sw.writerow(state)
			except UnicodeEncodeError:
				continue
			pass
		
	all_countries = '../data/ids_countries.json'
   
	with open('../data/ids_countries.json', 'w') as outfile:
		json.dump(ids_countries, outfile)
	
	print('done')
