#Based on example gapminder app from bokeh library 2019

from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker,
                          Slider, Button, Label, LabelSet, CategoricalColorMapper)

from bokeh.plotting import figure, output_file, show
from bokeh.models import MapOptions
from bokeh.tile_providers import OSM, get_provider

from converter import *
from node import Node
import pandas as pd
import numpy as np
import json
import random

#Colors shown in file palette_two.pdf
#agents_rim_color = '#f31649'#Deep Red

#Agent Type Colors
agents_color = '#ffffff' #White
homing_color = '#fbff00' #Yellow

#Rim Colors
aggressive_color = '#da3447' #Red
neutral_color = '#34c85d' #Green
careful_color = '#0044cc' #Blue

inactive_color = '#9421a1' #Magenta
crashed_color = '#747474' #Grey
reached_goal_color = '#ff7700' #Orange

#Map Elements Colors
streets_color = '#d3d3d3'   #Light Grey
nodes_color = '#ffffff'     #White
nodes_rim_color = '#d3d3d3'

def find_agents_with_type(df, type):
    df_result = df.loc[df['type'] == type]

    # TODO: check for empty df
    return df_result

def add_node_labels(self, x1, y1, nodes_ids):
    source = ColumnDataSource(data=dict(posX=x1, posY=y1, nodeids=nodes_ids))

    nodes_labels = LabelSet(x='posX', y='posY', text='nodeids', level='glyph',
          x_offset=5, y_offset=5, text_font_size="10pt", text_color="#0c0c0c",
           source=source, render_mode='canvas')
    plot.add_layout(nodes_labels)


c = Converter()
tile_provider = get_provider(OSM)

plot = figure(title='Traffic Sim', plot_width=600,  plot_height=600,
                x_range=c.convert_longitude_range(6.105, 6.13), y_range=c.convert_latitude_range(51.77, 51.788),
                x_axis_type="mercator", y_axis_type="mercator",
                #match_aspect = True , aspect_scale = 0.6,
                tools="pan, wheel_zoom, reset", active_drag="pan", active_scroll = "wheel_zoom")
#plot.add_tile(tile_provider) # Shows open maps in the background

#plot.xaxis.ticker = SingleIntervalTicker(interval=1)
plot.xaxis.axis_label = "Coordinate X longitude"
#plot.yaxis.ticker = SingleIntervalTicker(interval=1)
plot.yaxis.axis_label = "Coordinate Y latitude"

label = Label(x=9, y=2.5, text=str("Iteration"), text_font_size='30pt', text_color='#eeeeee')
plot.add_layout(label)




#Reading map.json and adding nodes on the display
with open('map.json') as f:
    map = json.load(f)

    node_list = list()

    x1 = list()
    y1 = list()
    nodes_ids = list()
    for node in map['nodes']:
        new_node = Node(node['X'], node['Y'], node['node_id'])
        new_node.connections = node['connections']
        node_list.append(new_node)
        x1.append(node['X'])
        y1.append(node['Y'])
        nodes_ids.append(node['node_id'])

    plot.circle(x1,y1,fill_color = nodes_color, line_color = nodes_rim_color, size=4)


    #Link nodes to each other
    for node in node_list:
        for id in node.connections:
            for other in node_list:
                if(other.node_id == id):
                    node.connected_nodes.append(other)
                    break
    #In order to draw one street only once, we have to remove drawn connections
    for node in node_list:
        for connected_node in node.connected_nodes:
            xa = [node.position.x, connected_node.position.x]
            ya = [node.position.y, connected_node.position.y]
            connected_node.remove_connected_node_with_id(node.node_id)
            plot.line(xa,ya,line_color = streets_color, line_width=3)
#---------------------------

#Reading data from agents.json
df_agents_file = pd.read_json("agents.json")
iter_max = df_agents_file.iloc[-1,0] #total number of iterations is +1
df_agents_file.set_index('iteration', inplace = True)
print('>> iter max: {}'.format(iter_max))
single_iteration_data = pd.DataFrame(df_agents_file.iat[0,0])

source_agents1 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'roaming'))
plot.circle(x = 'X',y = 'Y',fill_color= agents_color, line_color = neutral_color, size=5, source=source_agents1)

source_agents2 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'homing'))
plot.circle(x = 'X',y = 'Y',fill_color= homing_color, line_color = neutral_color, size=5, source=source_agents2)

source_agents3 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'crashed'))
plot.circle(x = 'X',y = 'Y',fill_color= agents_color, line_color = crashed_color, size=5, source=source_agents3)

source_agents4 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'aggressive_roaming'))
plot.circle(x = 'X',y = 'Y',fill_color= agents_color, line_color = aggressive_color, size=5, source=source_agents4)

source_agents5 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'careful_roaming'))
plot.circle(x = 'X',y = 'Y',fill_color= agents_color, line_color = careful_color, size=5, source=source_agents5)

## TODO: Homing Roaming and Homing

source_agents6 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'reached_goal'))
plot.circle(x = 'X',y = 'Y',fill_color= homing_color, line_color = reached_goal_color, size=5, source=source_agents6)

source_agents7 = ColumnDataSource (find_agents_with_type(single_iteration_data, 'inactive'))
plot.circle(x = 'X',y = 'Y',fill_color= homing_color, line_color = inactive_color, size=5, source=source_agents7)


def animate_update():
    iteration = slider.value + 1
    if iteration > iter_max:
        iteration = 0
    slider.value = iteration


def slider_update(attrname, old, new):
    iteration = slider.value
    label.text = "Iteration " + str(slider.value)

    df = pd.DataFrame(df_agents_file.iat[iteration,0])

    source_agents1.data = find_agents_with_type(df, 'roaming')
    source_agents2.data = find_agents_with_type(df, 'homing')
    source_agents3.data = find_agents_with_type(df, 'crashed')
    source_agents4.data = find_agents_with_type(df, 'aggressive_roaming')
    source_agents5.data = find_agents_with_type(df, 'careful_roaming')
    source_agents6.data = find_agents_with_type(df, 'reached_goal')
    source_agents7.data = find_agents_with_type(df, 'inactive')

slider = Slider(start=0, end=iter_max, value=1, step=1, title="Iteration")
slider.on_change('value', slider_update)

callback_id = None

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 30)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_click(animate)

layout = layout([
    [plot],
    [slider, button],
], sizing_mode='fixed')

curdoc().add_root(layout)
curdoc().title = "Traffic Sim"
show(layout)
