import pandas as pd
import numpy as np
import math, json
from pvector import Pvector

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
#from bokeh.palettes import GnBu
#from bokeh.transform import cumsum
from bokeh.layouts import gridplot

class AgentData(object):
    """Object for agent data extracted from json."""
    def __init__(self):
        pass


#begin here
plot_width = 450
plot_height = 450
agent_vision_range = 1

print('Check agents vision range')
df_agents_file = pd.read_json("agents.json")
df_agents_file.set_index('iteration', inplace = True)
iter_max = df_agents_file.last_valid_index() #total number of iterations is +1
print('>> iteration max: {}, total number is: {}'.format(iter_max, iter_max + 1))

df_first = pd.DataFrame(df_agents_file.iat[0,0])
agent_number_max = df_first.last_valid_index()
print('>> agent count is: {}'.format(agent_number_max + 1))

#Extract data from json file and create 2d array of AgentData objects
#across iterations (t) for all agents(j)
array_agents_data = list()
for t in range(0, iter_max + 1):
    df = pd.DataFrame(df_agents_file.iat[t,0])
    iteration_list = list()
    for j in range(0, agent_number_max + 1):
        agent = AgentData()
        agent.id = df.iat[j,0]
        agent.type = df.iat[j,1]
        agent.x = df.iat[j,2]
        agent.y = df.iat[j,3]
        iteration_list.append(agent)
    array_agents_data.append(iteration_list)

#Next lets calculate their separations for each agent between agents
# Numpy 3D array: Sets, Rows per Set, Columns
array_deltas = np.zeros((iter_max + 1, agent_number_max + 1, agent_number_max + 1))

#result is a stack of square matrices, each matrix corresponds to single iteration.
# Within square matrix you see magnitudes of vectors, that link every agent.
for t in range(0, iter_max + 1):

    for index, agent in enumerate(array_agents_data[t]):
        for index2, agent2 in enumerate(array_agents_data[t]):
            if(agent.id == agent2.id):
                array_deltas[t][index][index2] = 0
            else:
                delta_r = Pvector(agent2.x, agent2.y) - Pvector(agent.x, agent.y)
                #if delta_r.magnitude() < agent_vision:     #not sure how do range
                array_deltas[t][index][index2] = delta_r.magnitude()

#print(array_deltas)


#Now lets find mean separation for agents during each iteration
array_means = np.zeros((agent_number_max + 1, iter_max + 1))
for t in range (0, iter_max + 1):

    for row in range(0, agent_number_max + 1):
        sum = 0
        for column in range(0, agent_number_max + 1):
            sum += array_deltas[t][row][column]
        mean = sum / agent_number_max
        array_means[row][t] = mean

#print(array_means)
#Now mean across iterations
array_results = array_means.mean(axis = 1)

#print(array_results)

'''
# save data to json
with open('mean_separation.json', 'w') as f:
    json.dump(array_agents_data, f, indent = 2)
print('Data saved in mean_separation.json')
'''

# create a new plot, output to html file
output_file("mean_separation.html")

#-------------------------------------------------------------------
#-----------------------Mean Separation-----------------------------
#source4 = ColumnDataSource(data=dict(x_list=x_list, v_list=v_list))

p1 = figure(
    title="Mean Separation Bar Plot",
    plot_width=plot_width,
    plot_height=plot_height,
    x_range=[-0.5, agent_number_max + 0.5],
    #y_range=[min(v_list)*0.9, max(v_list)*1.2],
    x_axis_label='Agent id',
    y_axis_label='Mean Separation',
    #match_aspect = True , aspect_scale = 0.6,
    tools="save", active_drag=None, active_scroll = None)

source1 = ColumnDataSource(data=dict(posX=list(i for i in range(0, agent_number_max + 1)), posY=array_results))
p1.vbar(x='posX', top='posY', color = '#8BE7D0', width=0.9, source=source1)

# add some renderers
#string4 = 'Global Mean: {}'.format(round(mean_velocity,2))
#p4.line(x = list(range(-1, agent_number_max + 1)), y = mean_velocity, line_width=2, color = '#27C19A', legend_label=string2)
#p4.xgrid.grid_line_color = None
#p4.legend.background_fill_alpha = 0.4
#-------------------------------------------------------------------
plots = gridplot([[p1,None]], toolbar_location= "right")
show(plots)
