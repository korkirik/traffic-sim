#Based on example gapminder app from bokeh library 2019

from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker,
                          Slider, Button, Label, LabelSet, CategoricalColorMapper)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show

import pandas as pd
import numpy as np
import random


plot = figure(x_range=(-1, 17), y_range=(-12, 5), title='Traffic Sim', plot_height=450, match_aspect=True)
plot.xaxis.ticker = SingleIntervalTicker(interval=1)
plot.xaxis.axis_label = "Coordinate X longitude"
plot.yaxis.ticker = SingleIntervalTicker(interval=1)
plot.yaxis.axis_label = "Coordinate Y latitude"

label = Label(x=10.5, y=2, text=str("Iteration"), text_font_size='30pt', text_color='#eeeeee')
plot.add_layout(label)

#color_mapper = CategoricalColorMapper(palette=Spectral6, factors=regions_list)


#Reading data from mapFile with nodes coordinates and drawing it
df_mapFile = pd.read_csv("mapFile.csv")
x1 = df_mapFile.iloc[:,1]
y1 = df_mapFile.iloc[:,2]

plot.circle(x1,y1,fill_color='#7c7e71', size=4)

source = ColumnDataSource(df_mapFile)
labels = LabelSet(x=' X', y=' Y', text='# nodeId', level='glyph',
              x_offset=5, y_offset=5, text_font_size="10pt", text_color="#0c0c0c",
               source=source, render_mode='canvas')
plot.add_layout(labels)


#Reading data from agentsFile
df_agentsFile = pd.read_csv("agentsFile.csv")
iterMax = df_agentsFile.iloc[-1,0]

df_agentsFile.set_index('# iteration', inplace=True)

#Draw agents on the map TODO add random colors
source_agents = ColumnDataSource(df_agentsFile.loc[[0],:])
plot.circle(x = ' X',y = ' Y',fill_color='#20D0D9', size=4, source=source_agents)

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
    label.text = "Iteration"
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
