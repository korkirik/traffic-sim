from streetsegment import *
from node import *
from pvector import *
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import numpy as np

output_file("map_build_tg2.1.0.html")

class Map:
    def __init__(self):
        self.name = 'Default Map Name'
        self.node_list = list()

    def load_streets(self, recievedList):
        self.street_segment_list = recievedList.copy()

    def generate_nodes(self):
        length = len(self.street_segment_list)
        self.node_counter = 0
        for street_index in range(0,length,1):
            self.node_list.append(Node(
                self.street_segment_list[street_index].startPoint.x,
                self.street_segment_list[street_index].startPoint.y,
                self.node_counter))
            #self.node_list[self.node_counter].connectedStreetSegments.append(self.street_segment_list[street_index].name)
            self.node_counter += 1

            self.node_list.append(Node(
                self.street_segment_list[street_index].endPoint.x,
                self.street_segment_list[street_index].endPoint.y,
                self.node_counter))
            #self.node_list[self.node_counter].connectedStreetSegments.append(self.street_segment_list[street_index].name)

            self.node_list[self.node_counter - 1].connected_nodes.append(self.node_list[self.node_counter])
            self.node_list[self.node_counter].connected_nodes.append(self.node_list[self.node_counter - 1])

            self.node_counter += 1
        self.merge_nodes()

    def merge_nodes(self):
        rem = []
        for i in range(0,len(self.node_list)-1):
            for j in range(i + 1, len(self.node_list)):
                    if self.node_list[i].position.x == self.node_list[j].position.x:
                        if self.node_list[i].position.y == self.node_list[j].position.y:
                            self.node_list[i].connected_nodes = self.node_list[i].connected_nodes + self.node_list[j].connected_nodes

                            self.node_list[j].update_connections(self.node_list[i])    #updating links to new merged node
                            rem.append(self.node_list[j].node_id)

        self.nodes_created = len(self.node_list)

        mer = sorted(rem, reverse = True)
        self.node_list.reverse()
        self.deleted = 0
        for indexes_to_delete in mer:           #removing Nodes that repeat
            for obj in self.node_list:
                if(obj.node_id == indexes_to_delete):
                    self.node_list.remove(obj)
                    self.deleted += 1
                    break

    def get_node_list(self):
        return self.node_list

    def print_nodes_stats(self, showNodes):
        print('Nodes initially created: ', self.nodes_created)
        print('Nodes removed:', self.deleted)
        if(showNodes):
            for i in range(0,len(self.node_list)):
                print('Node:', self.node_list[i].node_id, 'Adjacent Nodes:')
                for j in range(0,len(self.node_list[i].connected_nodes)):
                    print(self.node_list[i].connected_nodes[j].node_id)

#Method used to visualise streets before interactive.py was implemented
#Currently not used # TODO: Factor the funtionality out into the interactive.py
    def draw_streets(self):
        p = figure(plot_width=700, plot_height=700, match_aspect=True)
        for node in self.node_list:
            for connected_node in node.connected_nodes: #Remove overlapping drawings
                x = [node.position.x, connected_node.position.x]
                y = [node.position.y, connected_node.position.y]
                p.line(x, y, line_width=2)

        for index in range(0,len(self.node_list), 1):
            x = self.node_list[index].position.x
            y = self.node_list[index].position.y
            p.circle(x, y, fill_color="white", size=2)

        source = ColumnDataSource(data=dict(posY=[o.position.y for o in self.node_list],
                                            posX=[o.position.x for o in self.node_list],
                                            nodeids=[o.node_id for o in self.node_list
                                                    ]))
        labels = LabelSet(x='posX', y='posY', text='nodeids', level='glyph',
              x_offset=5, y_offset=5, text_font_size="10pt", text_color="#0c0c0c",
               source=source, render_mode='canvas')
        p.add_layout(labels)
        show(p)

    def save_map_to_file(self):
        dataArray = np.zeros((len(self.node_list),3))
        #print(dataArray)
        #print(len(self.node_list))
        for rowIndex, node in enumerate(self.node_list):
            dataArray[rowIndex,0] = node.node_id
            dataArray[rowIndex,1] = node.position.x
            dataArray[rowIndex,2] = node.position.y
        #print(dataArray)
        np.savetxt("mapFile.csv", dataArray, delimiter=", ", header="node_id, X, Y")
