from map import *
from agent import *
from node import Node
from pvector import Pvector
import numpy as np
import random
import json
import math

from area import Area
from converter import *

class MapObject:
    def __init__(self, position, type, name):
        self.position = Pvector(0,0)
        self.position = position
        self.type = type
        self.name = name

class Simulation:
    def __init__(self):
        self.agent_count = 0
        self.agent_id = 0
        self.spawn_count = 0

        self.agent_list = list()
        self.free_node_list = list()

    def load_nodes(self, recieved_list):
        self.node_list = recieved_list
        self.free_node_list = recieved_list.copy() # TODO: temporary list remove

    def create_roaming_agents(self, number, type):
        for i in range(number):
            agent = Agent(self.agent_id, type)

            agent.set_starting_node(self.random_node_from_list_and_pop(self.free_node_list))
            agent.randomize_velocity()
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number

    def create_homing_agents(self, number, type): #, start_area, target_area):

        Area.set_all_node_list(self.node_list) # TODO: move into main
        area1 = Area(6.1287, 51.7943, 20)
        c = Converter()
        xn, yn = c.convert(6.128525, 51.7944791)
        n = self.closest_node(Pvector(xn,yn))

        for i in range(number):
            agent = Agent(self.agent_id, type)
            #Select a starting position and a target for homing agents here
            #agent.set_target_node(self.node_list[3])
            if(agent.type == 'bus'):
                agent.set_starting_node(self.random_node_from_list_and_pop(area1.node_list))
                agent.set_target_list(self.bus_stop_list)
                print('bus recieved a list of bus stops')
            else:
                #agent.set_starting_node(self.random_node_from_list_and_pop(area1.node_list))
                #setting starting position
                p = self.place_near_node(n)
                virtual_node = Node(p.x, p.y, 0)
                virtual_node.connected_nodes.append(n)
                agent.set_starting_node(virtual_node)
                agent.set_target_list(self.waypoint_list)
                agent.randomize_velocity()

            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1

        print('homing agents created {}'.format(number))
        self.agent_count += number

    def add_bus_stops(self):
        self.bus_stop_list = list()
        c = Converter()

        self.bus_stop_list.append(MapObject(c.convert_point(6.13014, 51.79376), 'bus_stop', 'Kleve Gruftstraße'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.138100038, 51.790521966), 'bus_stop','Kleve Koekkoek-Platz'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.1435, 51.791328), 'waypoint','Waypoint one'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.14441, 51.78984), 'waypoint','Waypoint two'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.14491, 51.790242), 'bus_stop','Kleve Bahnhof'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.14645, 51.79346), 'bus_stop','Hochschule'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.1487635, 51.7943618), 'waypoint','Waypoint three'))

        self.waypoint_list = self.bus_stop_list.copy()
        del self.waypoint_list[2:5]

        data = dict()
        element_list = list()
        data['bus_stops'] = element_list

        for index, o in enumerate(self.bus_stop_list):
            element = dict()
            element['type'] = o.type
            element['X'] = o.position.x
            element['Y'] = o.position.y
            element_list.append(element)

        with open('bus_stops.json', 'w') as f:
            json.dump(data, f, indent = 2)
        print('Bus stops saved')

    def place_near_node(self, n):
        p = Pvector(0,0)

        r = 20 + 10 * random.random()
        phi = (math.pi/3)*random.random()
        x = r*math.cos(phi)
        y = r*math.sin(phi)
        p = Pvector(x,y) + n.position
        return p

    def closest_node(self, point):
        minimum = None
        closest_node = None

        for node in self.node_list:
            d = node.position - point
            distance = d.magnitude()
            if(minimum == None or distance < minimum):
                minimum = distance
                closest_node = node

        return closest_node

    def random_node(self):
        l = len(self.node_list)
        node = self.node_list[random.randrange(0,l,1)]
        return node

    def random_node_from_list(self,list_):
        l = len(list_)
        node = list_[random.randrange(0,l,1)]
        return node

    def random_node_from_list_and_pop(self,list_):
        l = len(list_)
        n = random.randrange(0,l,1)
        return list_.pop(n)

    def start_simulation(self, time):
        self.iter_max = time

        it_list = list()
        agents_group = self.agent_list # TODO: expand to more groups

        for iter in range(0, self.iter_max, 1):
            it_data = dict()
            it_data['iteration'] = iter


            element_list = list()
            it_data['agents'] = element_list

            #add agents during simulation every 50 iterations
            if(iter % 50 == 0 and (iter < 260 or iter > 540)):
                if(self.spawn_count < 40):
                    self.create_homing_agents(1, 'homing')
                    self.spawn_count +=1

            for agentIndex, agent in enumerate(agents_group):
                element = dict()
                element['agent_id'] = agent.agent_id
                element['type'] = agent.agent_type
                element['X'] = agent.position.x
                element['Y'] = agent.position.y

                element_list.append(element)

                agent.update()

            it_list.append(it_data)

        print('Agents created: {}'.format(self.agent_count))
        with open('agents.json', 'w') as f:
            json.dump(it_list, f, indent = 2)
        print('Simulation complete, {} steps'.format(time))
