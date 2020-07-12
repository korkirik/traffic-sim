from streetsegment import *
from node import *
from pvector import *
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import numpy as np
import json

output_file("map_build_tg2.1.0.html")

class Map:
    def __init__(self):
        self.name = 'Default Map Name'
        self.node_list = list()

    def load_streets(self, recieved_list):
        self.street_segment_list = recieved_list.copy()

    def generate_nodes(self):
        length = len(self.street_segment_list)
        self.node_counter = 0
        for street_index in range(0,length,1):
            self.node_list.append(Node(
                self.street_segment_list[street_index].start_point.x,
                self.street_segment_list[street_index].start_point.y,
                self.node_counter))
            #self.node_list[self.node_counter].connectedStreetSegments.append(self.street_segment_list[street_index].name)
            self.node_counter += 1

            self.node_list.append(Node(
                self.street_segment_list[street_index].end_point.x,
                self.street_segment_list[street_index].end_point.y,
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

    def save_map_to_csv(self):
        dataArray = np.zeros((len(self.node_list),3))

        for rowIndex, node in enumerate(self.node_list):
            dataArray[rowIndex,0] = node.node_id
            dataArray[rowIndex,1] = node.position.x
            dataArray[rowIndex,2] = node.position.y

        np.savetxt("mapFile.csv", dataArray, delimiter=", ", header="node_id, X, Y")

    def save_graph_to_json(self):
        data = dict()
        element_list = list()

        for node in self.node_list:
            element = dict()
            element['node_id'] = node.node_id
            element['X'] = node.position.x
            element['Y'] = node.position.y
            element['connections'] = node.get_connections_ids()
            element_list.append(element)

        data['nodes'] = element_list

        with open('map.json', 'w') as f:
            json.dump(data, f, indent = 2)
