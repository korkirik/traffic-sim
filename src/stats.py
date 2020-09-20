import pandas as pd
import numpy as np
import math, json
from pvector import Pvector

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu
from bokeh.transform import cumsum
from bokeh.layouts import gridplot

def find_agent_across_iterations(df_agents_file, agent_id):

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

def count_agents_with_type(df, type):
    one_type_df = df.loc[df['type'] == type]
    one_type_df = one_type_df.reset_index(drop=True)
    if(one_type_df.last_valid_index() == None):
        d = {'type': [type], 'number': [0]}
    else:
        d = {'type': [type], 'number': [one_type_df.last_valid_index() + 1]}
    df_result = pd.DataFrame.from_dict(d)
    #print(df_result)
    return df_result

def find_agent_breakdown(df_agents_file, point):

    breakdown_df = pd.DataFrame(columns=['type', 'number'])
    if(point == 'start'):
        first_df = pd.DataFrame(df_agents_file.iat[0,0])
    elif(point == 'end'):
        first_df = pd.DataFrame(df_agents_file.iat[-1,0])

    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'homing')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'careful_homing')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'aggressive_homing')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'roaming')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'careful_roaming')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'aggressive_roaming')])

    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'crashed')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'inactive')])
    breakdown_df = pd.concat([breakdown_df, count_agents_with_type(first_df, 'reached_goal')])

    breakdown_df = breakdown_df.reset_index(drop=True)
    return breakdown_df



#begin here
plot_width = 450
plot_height = 450

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

    df = find_agent_across_iterations(df_agents_file, i)
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

#--------------------Agent Breakdown Chart -------------------------
data = find_agent_breakdown(df_agents_file, 'start')

data['angle'] = data['number']/data['number'].sum() * 2*math.pi
data['color'] = GnBu[len(data.index)]
data = data[data.number != 0]
print(data)
p3 = figure(
    title="Agent Breakdown Chart: Start",
    plot_width=plot_width,
    plot_height=plot_height,
    x_range=(-0.5, 1.0),
    toolbar_location=None,
    tools="hover",
    tooltips="@type: @number")

p3.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='type', source=data)

p3.axis.axis_label=None
p3.axis.visible=False
p3.grid.grid_line_color = None
#-------------------------------------------------------------------
#--------------------Agent Breakdown Chart End----------------------
data4 = find_agent_breakdown(df_agents_file, 'end')

data4['angle'] = data4['number']/data4['number'].sum() * 2*math.pi
data4['color'] = GnBu[len(data4.index)]
data4 = data4[data4.number != 0]
print(data4)
p4= figure(
    title="Agent Breakdown Chart: End",
    plot_width=plot_width,
    plot_height=plot_height,
    x_range=(-0.5, 1.0),
    toolbar_location=None,
    tools="hover",
    tooltips="@type: @number")

p4.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='type', source=data4)

p4.axis.axis_label=None
p4.axis.visible=False
p4.grid.grid_line_color = None
#-------------------------------------------------------------------
plots = gridplot([[p1, p2, p3, p4], [None, None, None]], toolbar_location= "right")
show(plots)
