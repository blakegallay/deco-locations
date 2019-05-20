#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:11:06 2017

@author: patron
"""
'''
>>> from geopy.geocoders import Nominatim
>>> geolocator = Nominatim()
>>> location = geolocator.geocode("175 5th Avenue NYC")
>>> print(location.address)
Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
>>> print((location.latitude, location.longitude))
(40.7410861, -73.9896297241625)
>>> print(location.raw)
'''


import gmplot
import csv
import geopy
from geopy.geocoders import Nominatim
from colour import Color
import certifi
from math import *
import math
import urllib
#import cartopy.crs as ccrs
#import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab as pl
import numpy as np
import mpld3
import matplotlib.image as mpimg

countries = {}
ccountries = {}
cap = {}
coords = []
with open('/data/contributingCountries.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        r = 0
        try:
            for row in reader:
                if r < 196:
                    countries[row[0]] = row[1]
                    ccountries[row[0]] = row[2]
                    cap[row[0]] = float(row[1]) / float(row[3])
                r += 1
                if(r > 196):
                    break
                #print(cap[row[0]])
        except UnicodeDecodeError:
            pass
print('opened countries.csv')
with open('/data/gridCoords.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        try:
            for row in reader:
                coords.append(row)
                
        except UnicodeDecodeError:
            pass
print('opened gridcoords.csv')
colors = {}
red = Color("black")
colorRange = list(red.range_to(Color("white"),5))

for count in ccountries:
    if(countries[count] != '0'):
        colors[count] = str(colorRange[int(math.log(cap[count], 10) * -1 / 2)])
        print(int(math.log(cap[count], 10) * -1 / 2))
print('counted ccountries')
def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)
geolocator=Nominatim(timeout=3)
geolocator.urlopen = uo
keys = []
k = 0
for key in countries:
    keys.append(key)

gmap = gmplot.GoogleMapPlotter(0, 0, 2)

gmap2 = gmplot.GoogleMapPlotter(0,0,2)
gmap3 = gmplot.GoogleMapPlotter(0,0,2)

for c in coords:
    print(c)
    gmap3.scatter([float(c[0])], [float(c[1])], 'k', 50000, marker=False)
gmap3.draw('/html/coords_map.html')
print('went through c in coords')
for country in countries:
    
    if(countries[country] != '0'):
        radius = int(countries[country]) * 2 + 200000
        gmap.scatter([geolocator.geocode(country).latitude], [geolocator.geocode(country).longitude], colors[country], radius, marker=False)
        gmap2.scatter([geolocator.geocode(country).latitude], [geolocator.geocode(country).longitude], 'FFF4500', str(country + " - " + countries[country] + " events"), marker=True)
print('scattered')
lats = []
lons = []
for coordinate in coords:
    lats += [float(coordinate[0])]
    lons += [float(coordinate[1])]
print('got latlons')
#gmap.heatmap(lats,lons)
gmap.draw("/html/circleMap.html")
gmap2.draw('/html/pinsMap.html')

topCountries = []
with open('/data/topOfWeek.csv', newline='') as top:
        reader = csv.reader(top, delimiter=',')
        try:
            for row in reader:
                topCountries.append([row[0],row[1]])         
        except UnicodeDecodeError:
            pass
print('got topofweek')
while(len(topCountries) < 10):
    topCountries.append(['---','---'])

welcome = {}

with open('languages.csv', newline='') as lang:
    lreader = csv.reader(lang, delimiter=',')
    try:
        for row in lreader:
            welcome[row[0]] = row[1]
    except UnicodeDecodeError:
        pass
print('got languages')
states = 0
with open('/data/states.csv', newline='') as states:
    reader = csv.reader(states, delimiter=",")
    cont = True
    for row in reader:
        if(cont):
            states = int(row[0])
            cont = False
        
print('got states')
t = open('/html/Leaderboard-month.html','w')

t.write("<!DOCTYPE html>\n")
t.write("<html>")
t.write("<head><title>Top Contributors Table</title></head>")
t.write("<body>")
t.write("<style>")
t.write("	table{")
t.write("	border: 1px solid black;")
t.write("	text-align: center;")
t.write("}")
t.write("	td{")
t.write("	border: 1px: solid black;")
t.write("}")
t.write("</style>")
t.write("<linktype='text/css' rel='stylesheet' href='Tablestyle.css'/>")
t.write("	<table style='Border: Solid Black'>")
t.write("		<thead>")
t.write("			<tr>")
t.write("				<th colspan='3'>Top Contributors of the Month</th>")
t.write("			</tr>")
t.write("			<tr style='border: 1px Solid Black'>")
t.write("				<th>Rank  </th>")
t.write("				<th>Country  </th>")
t.write("				<th>Number of events</th>")
t.write("			</tr>")
t.write("			<tr>")
t.write("				<td>1</td>")
t.write("				<td id='firstPlace'>"+topCountries[0][1]+"</td>")
t.write("				<td>"+topCountries[0][0]+"</td>")
t.write("			</tr>")
t.write("			<tr>")
t.write("				<td>2</td>")
t.write("				<td id='secondPlace'>"+topCountries[1][1]+"</td>")
t.write("				<td>"+topCountries[1][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>3</td>")
t.write("				<td id='thirdPlace'>"+topCountries[2][1]+"</td>")
t.write("				<td>"+topCountries[2][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>4</td>")
t.write("				<td id='fourthPlace'>"+topCountries[3][1]+"</td>")
t.write("				<td>"+topCountries[3][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>5</td>")
t.write("				<td id='fifthPlace'>"+topCountries[4][1]+"</td>")
t.write("				<td>"+topCountries[4][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>6</td>")
t.write("				<td id='sixthPlace'>"+topCountries[5][1]+"</td>")
t.write("				<td>"+topCountries[5][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>7</td>")
t.write("				<td id='seventhPlace'>"+topCountries[6][1]+"</td>")
t.write("				<td>"+topCountries[6][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>8</td>")
t.write("				<td id='eighthPlace'>"+topCountries[7][1]+"</td>")
t.write("				<td>"+topCountries[7][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>9</td>")
t.write("				<td id='ninthPlace'>"+topCountries[8][1]+"</td>")
t.write("				<td>"+topCountries[8][0]+"</td>")
t.write("			</tr>	")
t.write("			<tr>")
t.write("				<td>10</td>")
t.write("				<td id='tenthPlace'>"+topCountries[9][1]+"</td>")
t.write("				<td>"+topCountries[9][0]+"</td>")
t.write("			</tr>		")
t.write("		</thead>")
t.write("	</table>")
t.write("</html>")

t.close()
print('wrote monthtop')
topAll = []

with open('/data/topCountries.csv', newline='') as all:
        readera = csv.reader(all, delimiter=',')
        try:
            for row in readera:
                if(row[0] != '0'):
                    topAll.append([row[1],row[0]])         
        except UnicodeDecodeError:
            pass
print('read topofall')
g = open('/html/Leaderboard.html','w')

g.write("<!DOCTYPE html>\n")
g.write("<html>")
g.write("<head><title>Top Contributors Table</title></head>")
g.write("<body>")
g.write("<style>")
g.write("	table{")
g.write("	border: 1px solid black;")
g.write("	text-align: center;")
g.write("}")
g.write("	td{")
g.write("	border: 1px: solid black;")
g.write("}")
g.write("</style>")
g.write("<linktype='text/css' rel='stylesheet' href='Tablestyle.css'/>")
g.write("	<table style='Border: Solid Black'>")
g.write("		<thead>")
g.write("			<tr>")
g.write("				<th colspan='3'>"+str(states)+"/50 US States and "+str(len(topAll))+"/195 Countries<br /> have contributed to DECO<br /><br />Top Contributors of All Time</th>")
g.write("			</tr>")
g.write("			<tr style='border: 1px Solid Black'>")
g.write("				<th>Rank  </th>")
g.write("				<th>Country  </th>")
g.write("				<th>Number of events</th>")
g.write("			</tr>")

for c in range(len(topAll)):

	g.write("               <tr>")
	g.write("				<td>"+str(c+1)+"</td>")
	g.write("				<td id='"+str(c+1)+"thPlace'>"+topAll[c][0]+"</td>")
	g.write("				<td>"+topAll[c][1]+"</td>")
	g.write("			    </tr>")

g.write("		</thead>")
g.write("	</table>")
g.write("</html>")
print('wrote topofall')
g.close()
newcountry = ""
with open('/data/newCountries.csv', newline='') as new:
        readern = csv.reader(new, delimiter=',')
        try:
            for row in readern:
                for n in topAll:
                    if n[0] == row[0] and n[0] != "0":
                        newcountry = row[0]      
        except UnicodeDecodeError:
            pass
print('got newcountry')
n = open('/html/welcome.html','w')


n.write("<!DOCTYPE html>\n")
n.write('<html><h5 style="margin-bottom:5px;">'+welcome[newcountry]+' (Welcome) to the Newest Contributor:</h5><h3 style="display:inline;margin-left:40px">'+newcountry+'</h3>     <div style="display:inline-block;text-align: left;"><IMG style="width:55px;height:36px" SRC="./Flags/'+newcountry+'.png" ALT="image"></div></html>')
n.close()
print('wrote welcome')
'''
c_numero = []
unique_pais = []
for country in countries:
	unique_pais.append(country)
	c_numero.append(float(countries[country]))
maximo = max(c_numero)
cmap = mpl.cm.Blues
test = 0
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)
fig = pl.figure()
rect = 0.1, 0.1, 0.8, 0.8
ax = fig.add_subplot(111, projection=ccrs.Robinson())
for country in shpreader.Reader(countries_shp).records():
    nome = country.attributes['name_long']
    print(nome)
    if nome in unique_pais:
        i = unique_pais.index(nome)
        numero = c_numero[i]
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),facecolor=cmap(math.sqrt(math.sqrt(numero / float(maximo))), 1.01),label=nome)
        print("drew...")

    else:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor='#FAFAFA',
                              label=nome)

if test != len(unique_pais):
    print("check the way you are writting your country names!")
plt.show()
plt.savefig('test.png')
#mpld3.save_html(pl.gcf(),'countrymap.html')
#mpimg.imsave("out.png", fig)'''
print('done')