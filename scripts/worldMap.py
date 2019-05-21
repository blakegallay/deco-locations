from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LogColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.embed import file_html
from bokeh.resources import CDN
import geopandas as gpd
import pandas as pd
import csv
import json
from math import *

from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

shapefile = '../misc/country_shapes/ne_110m_admin_0_countries.shp'

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

gdf.columns = ['country', 'country_code', 'geometry']

deco_countries_path = '../data/contributingCountries.csv'

df = pd.read_csv(deco_countries_path, names=['events','percent', 'population'])
df.index.name = 'country'

df.drop(['percent'], axis=1)
df.drop(['population'], axis=1)


merged = gdf.merge(df, left_on='country', right_on='country', how='left')

json_data = json.loads(merged.to_json())

json_data = json.dumps(json_data)

geosource = GeoJSONDataSource(geojson = json_data)
palette = brewer['YlGnBu'][8]

palette = palette[::-1]

color_mapper = LogColorMapper(palette = palette, low = 0, high = 300000)

hover = HoverTool(tooltips = [ ('Country','@country'),('# Events', '@events')])

p = figure(title='DECO Data Taking Locations', plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
p.xgrid.grid_line_color=None
p.ygrid.grid_line_color=None

p.axis.visible = False

p.patches('xs','ys', source = geosource,fill_color = {'field' :'events', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

output_file("../html/worldMap.html")	  
		  
html = file_html(p, CDN, "map")

show(p)

	



