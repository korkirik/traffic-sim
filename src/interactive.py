#Based on example gapminder app from bokeh library 2019

from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker,
                          Slider, Button, Label, LabelSet, CategoricalColorMapper)
#from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show

from node import *
import pandas as pd
import numpy as np
import json
import random


plot = figure(x_range=(-1, 17), y_range=(-12, 5), title='Traffic Sim', plot_height=600, match_aspect=True,
                tools="pan, wheel_zoom, reset", active_drag="pan", active_scroll = "wheel_zoom")

#plot = figure(title='Traffic Sim', plot_height=450, match_aspect=True)
plot.xaxis.ticker = SingleIntervalTicker(interval=1)
plot.xaxis.axis_label = "Coordinate X longitude"
plot.yaxis.ticker = SingleIntervalTicker(interval=1)
plot.yaxis.axis_label = "Coordinate Y latitude"

label = Label(x=9, y=2.5, text=str("Iteration"), text_font_size='30pt', text_color='#eeeeee')
plot.add_layout(label)


#Reading graph.json and adding nodes on the display
with open('graph.json') as f:
    graph = json.load(f)

    node_list = list()

    x1 = list()
    y1 = list()
    for node in graph['nodes']:
        new_node = Node(node['X'], node['Y'], node['node_id'])
        new_node.connections = node['connections']
        node_list.append(new_node)
        x1.append(node['X'])
        y1.append(node['Y'])

    plot.circle(x1,y1,fill_color='#00ff00', size=10)

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
            plot.line(xa,ya,line_color='#ff5656', line_width=2)
'''Labels
source = ColumnDataSource(data=dict(posY=[o.position.y for o in self.node_list],
                                    posX=[o.position.x for o in self.node_list],
                                    nodeids=[o.node_id for o in self.node_list
                                            ]))
labels = LabelSet(x='posX', y='posY', text='nodeids', level='glyph',
      x_offset=5, y_offset=5, text_font_size="10pt", text_color="#0c0c0c",
       source=source, render_mode='canvas')
plot.add_layout(labels)'''
#---------------------------

#Reading data from agentsFile
df_agentsFile = pd.read_csv("agentsFile.csv")
iterMax = df_agentsFile.iloc[-1,0]

df_agentsFile.set_index('# iteration', inplace=True)

#Draw agents on the map TODO add random colors
source_agents = ColumnDataSource(df_agentsFile.loc[[0],:])
plot.circle(x = ' X',y = ' Y',fill_color='#ffff00', line_color = '#00ff1a', size=6, source=source_agents)

#plot.line(xa,ya,line_color='#a6051a', line_width=2, line_dash= 'dashed')
#print(iterMax)
#plot.add_tools(HoverTool(tooltips="@Country", show_arrow=False, point_policy='follow_mouse'))


def animate_update():
    iteration = slider.value + 1
    if iteration > iterMax:
        iteration = 0
    slider.value = iteration


def slider_update(attrname, old, new):
    iteration = slider.value
    label.text = "Iteration " + str(slider.value)
    source_agents.data = df_agentsFile.loc[[iteration],:]

slider = Slider(start=0, end=iterMax, value=1, step=1, title="Iteration")
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
show(plot)
