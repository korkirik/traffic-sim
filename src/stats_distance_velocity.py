import pandas as pd
import numpy as np
import math, json
from pvector import Pvector

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu
from bokeh.transform import cumsum
from bokeh.layouts import gridplot

def find_mean(list, count):
    sum = 0
    for value in list:
        sum += value
    mean_value = sum/count
    return mean_value


plot_width = 450
plot_height = 450

df_stats_file = pd.read_json("stats.json")
agent_count = df_stats_file.last_valid_index() + 1 #total number
print('>> agent_count: {}'.format(agent_count))

x_list = list()
v_list = list()
dist_list = list()

print(df_stats_file)

for t in range(0, agent_count):
    x_list.append(df_stats_file.iat[t,0])
    dist_list.append(df_stats_file.iat[t,1])
    v_list.append(df_stats_file.iat[t,2])

print(x_list)
print(v_list)
print(dist_list)


mean_distance = find_mean(dist_list, agent_count)
mean_velocity = find_mean(v_list, agent_count)

output_file("stats.html")
#-------------------Distances Plot -------------------------------
source1 = ColumnDataSource(data=dict(x_list=x_list, dist_list=dist_list))

p1 = figure(
    title="Distances Bar Plot",
    plot_width=plot_width,
    plot_height=plot_height,
    x_range=[-0.5, len(x_list)],
    y_range=[min(dist_list)*0.95, max(dist_list)*1.15],
    x_axis_label='Agent id',
    y_axis_label='Distance',
    #match_aspect = True , aspect_scale = 0.6,
    tools="save", active_drag=None, active_scroll = None)
p1.vbar(x='x_list', top='dist_list', color = '#8BE7D0', width=0.9, source=source1)

# add some renderers
string1 = 'Global Mean: {}'.format(round(mean_distance,2))
p1.line(x = list(range(-1, agent_count + 1)), y = mean_distance, line_width=2, color = '#27C19A', legend_label=string1)
p1.xgrid.grid_line_color = None
p1.legend.background_fill_alpha = 0.4
#legend customisation
#p1.legend.label_standoff = 50
#p1.legend.margin = 50
#p1.legend.padding = 50
#-------------------Velocities Plot -------------------------------
source2 = ColumnDataSource(data=dict(x_list=x_list, v_list=v_list))

p2 = figure(
    title="Mean Velocities Bar Plot",
    plot_width=plot_width,
    plot_height=plot_height,
    x_range=[-0.5, len(x_list)],
    y_range=[min(v_list)*0.9, max(v_list)*1.2],
    x_axis_label='Agent id',
    y_axis_label='Mean Velocity',
    #match_aspect = True , aspect_scale = 0.6,
    tools="save", active_drag=None, active_scroll = None)
p2.vbar(x='x_list', top='v_list', color = '#8BE7D0', width=0.9, source=source2)

# add some renderers
string2 = 'Global Mean: {}'.format(round(mean_velocity,2))
p2.line(x = list(range(-1, agent_count + 1)), y = mean_velocity, line_width=2, color = '#27C19A', legend_label=string2)
p2.xgrid.grid_line_color = None
p2.legend.background_fill_alpha = 0.4


plots = gridplot([[p1, p2], [None, None]], toolbar_location= "right")
show(plots)
