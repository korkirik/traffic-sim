from converter import Converter
from pvector import Pvector
from node import Node

class Area:

    @classmethod
    def set_all_node_list(cls, list):
        cls.all_node_list = list

    def __init__(self, long, lat, radius):
        self.node_list = list()
        self.agent_list = list()

        c = Converter()
        x,y = c.convert(long, lat) #(6.11, 51.7805)
        self.find_nodes(x,y,radius)
        print('Nodes in area: {}'.format(len(self.node_list)) )

    def find_nodes(self, x, y, radius):
        if(len(Area.all_node_list) == 0):
            print('class variable all_node_list is empty')

        center = Pvector(x,y)
        for node in Area.all_node_list:
            distance_vector = node.position - center
            distance = distance_vector.magnitude()
            if(distance <= radius):
                self.node_list.append(node)
