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
        area1 = Area(6.130314, 51.794326, 200)
        area2 = Area(6.14, 51.78, 200)

        for i in range(number):
            agent = Agent(self.agent_id, type)
            #agent.set_starting_node(self.random_node_from_list_and_pop(self.free_node_list))

            #Select a target for homing agents here
            #agent.set_target_node(self.node_list[3]) # self.node_list[100]
            # TODO: remove this if block
            '''
            if(len(nodes_in_area1) < 1):
                break
            '''

            agent.set_starting_node(self.random_node_from_list_and_pop(area1.node_list)) #self.free_node_list
            agent.set_target_node(self.random_node_from_list(self.node_list)) #area2.node_list)) #self.node_list[0]

            agent.randomize_velocity()
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1

        print('homing agents created {}'.format(number))
        self.agent_count += number

    def add_bus_stops(self):
        self.bus_stop_list = list()
        c = Converter()

        self.bus_stop_list.append(MapObject(c.convert_point(6.130150214491974,51.79382451156521), 'bus_stop', 'Kleve Gruftstraße'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.138115701747227,51.790514881124665), 'bus_stop','Kleve Koekkoek-Platz'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.145389852402583, 51.78991430122071), 'bus_stop','Kleve Bahnhof'))
        self.bus_stop_list.append(MapObject(c.convert_point(6.146449325029877, 51.793429736876085), 'bus_stop','Hochschule'))
        #self.bus_stop_list.append(MapObject(c.convert_point(6.1524521086094595, 51.79567091213551), 'bus_stop','Kleve Schulstraße'))

        for a in self.agent_list:
            if(a.type == 'bus'):
                #a.bus_stop_list = self.bus_stop_list
                print('buses recieved bus stops')

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

    def create_walker(self, number, area):
        for i in range(number):
            walker = Agent(self.agent_id, 'walker')
            self.agent_list.append(walker)
            walker.add_agent_list(self.agent_list)

            r = area.radius*random.random()
            phi = 2*math.pi*random.random()
            x = r*math.cos(phi)
            y = r*math.sin(phi)
            walker.position = Pvector(x,y)
            node = self.closest_node(walker.position)
            walker.set_closest_node(node)
            self.agent_id +=1

        self.agent_count += number

    def create_roaming_walker(self, number, area):
        for i in range(number):
            walker = Agent(self.agent_id, 'walkerroaming')
            self.agent_list.append(walker)
            walker.add_agent_list(self.agent_list)
            walker.my_behaviour.set_roaming_area(Pvector(area.x, area.y), area.radius)

            r = area.radius*random.random()
            phi = 2*math.pi*random.random()
            x = r*math.cos(phi)
            y = r*math.sin(phi)
            walker.position = Pvector(x,y)
            node = self.closest_node(walker.position)
            walker.set_closest_node(node)
            self.agent_id +=1

        self.agent_count += number
#for walkers
    def create_curiosities(self, number):
        self.curiosity_list = list()
        for i in range(number):
            cur = MapObject('curiosity')
            #self.agent_list.append(cur)
            self.curiosity_list.append(cur)

            r = 0.5 + 1 * random.random()
            phi = 2*math.pi*random.random()
            x = r*math.cos(phi)
            y = r*math.sin(phi)
            node = self.random_node()
            cur.position = Pvector(x,y) + node.position
            #self.agent_id +=1
        #self.agent_count += number

        for a in self.agent_list:
            a.curiosity_list = self.curiosity_list
#for walkers
    def create_destinations(self, number):
        self.destination_list = list()
        for i in range(number):
            dest = MapObject('destination')
            #self.agent_list.append(dest)
            self.destination_list.append(dest)

            r = 0.5 + 1 * random.random()
            phi = 2*math.pi*random.random()
            x = r*math.cos(phi)
            y = r*math.sin(phi)
            node = self.random_node()
            dest.position = Pvector(x,y) + node.position
            #self.agent_id +=1
        #self.agent_count += number

        for a in self.agent_list:
            a.dest_list = self.destination_list


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

#for walkers
    def save_map_objects_json(self):
        data = dict()
#code smell
        element_list = list()
        data['destinations'] = element_list

        for index, o in enumerate(self.destination_list):
            element = dict()
            element['type'] = o.type
            element['X'] = o.position.x
            element['Y'] = o.position.y
            element_list.append(element)

        element_list2 = list()
        data['curiosities'] = element_list2

        for index, o in enumerate(self.curiosity_list):
            element = dict()
            element['type'] = o.type
            element['X'] = o.position.x
            element['Y'] = o.position.y
            element_list2.append(element)

        with open('map_objects.json', 'w') as f:
            json.dump(data, f, indent = 2)
        print('Map objects saved')
#for walkers
    def read_additional_objects(self):
        with open('map_objects.json') as f:
            map_objects = json.load(f)

            self.curiosity_list = list()
            for o in map_objects['curiosities']:
                new_node = MapObject(o['type'])
                new_node.position = Pvector(o['X'], o['Y'])
                self.curiosity_list.append(new_node)

            self.destination_list = list()
            for o in map_objects['destinations']:
                new_node = MapObject(o['type'])
                new_node.position = Pvector(o['X'], o['Y'])
                self.destination_list.append(new_node)

    def start_simulation(self, time):
        #self.save_map_objects_json() Uncomment when launching walkers
        self.iter_max = time

        it_list = list()
        agents_group = self.agent_list # TODO: expand to more groups

        for iter in range(0, self.iter_max, 1):
            it_data = dict()
            it_data['iteration'] = iter


            element_list = list()
            it_data['agents'] = element_list

            for agentIndex, agent in enumerate(agents_group):
                element = dict()
                element['agent_id'] = agent.agent_id
                element['type'] = agent.agent_type
                element['X'] = agent.position.x
                element['Y'] = agent.position.y

                element_list.append(element)

                agent.update()

            it_list.append(it_data)


        with open('agents.json', 'w') as f:
            json.dump(it_list, f, indent = 2)
        print('Simulation complete, {} steps'.format(time))

    ## TODO: move agents' tests into other class
    def do_agent_tests(self):
        agent_tester = Agent_test(self.agent_list[0])
        #agent_tester.print_street_size()
        agent_tester.print_forces()
