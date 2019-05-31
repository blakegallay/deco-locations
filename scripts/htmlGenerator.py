#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gmplot
import csv
import geopy
from geopy.geocoders import Nominatim
from colour import Color
import certifi
from math import *
import math
import urllib
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
with open('../data/contributingCountries.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        r = 0
        try:
            for row in reader:
                if r < 196:
                    countries[row[0]] = row[1]
                r += 1
                if(r > 196):
                    break

        except UnicodeDecodeError:
            pass

colors = {}
red = Color("black")
colorRange = list(red.range_to(Color("white"),5))

topCountries = []
with open('../data/topOfMonth.csv', newline='') as top:
        reader = csv.reader(top, delimiter=',')
        try:
            for row in reader:
                topCountries.append([row[0],row[1]])         
        except UnicodeDecodeError:
            pass

while(len(topCountries) < 10):
    topCountries.append(['---','---'])

welcome = {}

with open('../data/languages.csv', newline='') as lang:
    lreader = csv.reader(lang, delimiter=',')
    try:
        for row in lreader:
            welcome[row[0]] = row[1]
    except UnicodeDecodeError:
        pass

with open('../data/states.csv', newline='') as states:
    reader = csv.reader(states, delimiter=",")
    state_count = 0
    for row in reader:
        if(row[1] != "0" and row[1] != "Event Count"):
	        state_count += 1
        
t = open('../html/Leaderboard-month.html','w')

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
t.write("				<th>Events</th>")
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
t.write("<html>")

t.close()

topAll = []

with open('../data/topCountries.csv', newline='') as all:
        readera = csv.reader(all, delimiter=',')
        try:
            for row in readera:
                if(row[0] != '0'):
                    topAll.append([row[1],row[0]])         
        except UnicodeDecodeError:
            pass

g = open('../html/Leaderboard.html','w')

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
g.write("				<th colspan='3'>"+str(state_count)+"/50 US States and "+str(len(topAll))+"/195 Countries<br /> have contributed to DECO<br /><br />Top Contributors of All Time</th>")
g.write("			</tr>")
g.write("			<tr style='border: 1px Solid Black'>")
g.write("				<th>Rank  </th>")
g.write("				<th>Country  </th>")
g.write("				<th>Events</th>")
g.write("			</tr>")

for c in range(len(topAll)):

	g.write("               <tr>")
	g.write("				<td>"+str(c+1)+"</td>")
	g.write("				<td id='"+str(c+1)+"thPlace'>"+topAll[c][0]+"</td>")
	g.write("				<td>"+topAll[c][1]+"</td>")
	g.write("			    </tr>")

g.write("		</thead>")
g.write("	</table>")
g.write("<html>")

g.close()
newcountry = ""
with open('../data/newCountries.csv', newline='') as new:
        readern = csv.reader(new, delimiter=',')
        try:
            for row in readern:
                for n in topAll:
                    if n[0] == row[0] and n[0] != "0":
                        newcountry = row[0]      
        except UnicodeDecodeError:
            pass

n = open('../html/welcome.html','w')

n.write("<!DOCTYPE html>\n")
n.write('<html><h5 style="margin-bottom:5px;">'+welcome[newcountry]+' (Welcome) to the Newest Contributor:</h5><h3 style="display:inline;margin-left:40px">'+newcountry+'</h3>     <div style="display:inline-block;text-align: left;"><IMG style="width:55px;height:36px" SRC="../Flags/'+newcountry+'.png" ALT="image"></div><html>')
n.close()