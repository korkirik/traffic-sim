import pandas as pd
import numpy as np
import json
from pvector import Pvector

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
#from bokeh.palettes import PuBu5
from bokeh.layouts import gridplot

def filter_agent_with_id(df_agents_file, agent_id):

    agent_complete_df = pd.DataFrame(columns=['agent_id', 'type', 'X', 'Y'])
    iter_max = df_agents_file.last_valid_index() #total number of iterations is +1
    for i in range(0, iter_max + 1, 1):
        df = pd.DataFrame(df_agents_file.iat[i,0])
        agent_in_one_iter_df = df.loc[df['agent_id'] == agent_id]
        agent_complete_df = pd.concat([agent_complete_df, agent_in_one_iter_df], ignore_index=True)

    #print('>> {}'.format(agent_complete_df))
    return agent_complete_df

def calculate_distance_mean_velocity(df):

    iter_max = df.last_valid_index() #total number of iterations is +1
    distance = 0
    for i in range(0,iter_max, 1):
        p1 = Pvector(df.iat[i,2],df.iat[i,3])
        p2 = Pvector(df.iat[i+1,2],df.iat[i+1,3])
        p = p2 - p1
        distance = distance + p.magnitude()
    mean_v = distance / (iter_max)
    #print('distance: {}, mean v: {}'.format(distance, mean_v))
    return distance, mean_v

def find_mean(list, count):
    sum = 0
    for value in list:
        sum += value
    mean_value = sum/count
    return mean_value

#begin here
df_agents_file = pd.read_json("agents.json")
df_agents_file.set_index('iteration', inplace = True)
iter_max = df_agents_file.last_valid_index() #total number of iterations is +1
print('>> iteration max: {}, total number is: {}'.format(iter_max, iter_max + 1))

df_first = pd.DataFrame(df_agents_file.iat[0,0])
agent_count = df_first.last_valid_index() + 1
print('>> agent count is: {}'.format(agent_count))

element_list = list()
x_list = list()
v_list = list()
dist_list = list()

for i in range(0, agent_count, 1):
    element = dict()
    element['agent_id'] = i

    df = filter_agent_with_id(df_agents_file, i)
    distance, mean_v = calculate_distance_mean_velocity(df)

    element['distance'] = distance
    element['mean_v'] = mean_v

    element_list.append(element)


    x_list.append(i)
    v_list.append(mean_v)
    dist_list.append(distance)
#print(element_list)

mean_distance = find_mean(dist_list, agent_count)
mean_velocity = find_mean(v_list, agent_count)

# save data to json
with open('stats.json', 'w') as f:
    json.dump(element_list, f, indent = 2)
print('Data saved in stats.json')


# create a new plot, output to html file
output_file("stats.html")
#-------------------Distances Plot -------------------------------
source1 = ColumnDataSource(data=dict(x_list=x_list, dist_list=dist_list))

p1 = figure(
    title="Distances Bar Plot",
    plot_width=600,
    plot_height=600,
    x_range=[-0.5, len(x_list)],
    y_range=[round(min(dist_list)*0.95), round(max(dist_list)*1.05)],
    x_axis_label='Agent id',
    y_axis_label='Distance',
    #match_aspect = True , aspect_scale = 0.6,
    tools="save", active_drag=None, active_scroll = None)
p1.vbar(x='x_list', top='dist_list', color = '#8BE7D0', width=0.9, source=source1)

# add some renderers
string1 = 'Global Mean: {}'.format(round(mean_distance,2))
p1.line(x = list(range(-1, agent_count + 1)), y = mean_distance, line_width=2, color = '#27C19A', legend_label=string1)
p1.xgrid.grid_line_color = None

#-------------------Velocities Plot -------------------------------
source2 = ColumnDataSource(data=dict(x_list=x_list, v_list=v_list))

p2 = figure(
    title="Mean Velocities Bar Plot",
    plot_width=600,
    plot_height=600,
    x_range=[-0.5, len(x_list)],
    y_range=[min(v_list)*0.9, max(v_list)*1.1],
    x_axis_label='Agent id',
    y_axis_label='Mean Velocity',
    #match_aspect = True , aspect_scale = 0.6,
    tools="save", active_drag=None, active_scroll = None)
p2.vbar(x='x_list', top='v_list', color = '#8BE7D0', width=0.9, source=source2)

# add some renderers
string2 = 'Global Mean: {}'.format(round(mean_velocity,2))
p2.line(x = list(range(-1, agent_count + 1)), y = mean_velocity, line_width=2, color = '#27C19A', legend_label=string2)
p2.xgrid.grid_line_color = None
#------------------------------------------------------------------


plots = gridplot([[p1, p2]], toolbar_location= "right")
show(plots)
