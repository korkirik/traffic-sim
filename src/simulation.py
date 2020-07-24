from map import *
from agent import *
from homing_agent import *
from node import Node
import numpy as np
import random
import json

from area import Area

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

        Area.set_node_list(self.node_list) # TODO: move into main
        area = Area(6.124, 51.78, 100)

        for i in range(number):
            agent = Agent(self.agent_id, type)
            #agent.set_starting_node(self.node_list[i])
            #agent.set_target_node(self.node_list[3]) # self.node_list[100]
            # TODO: remove this if block
            '''
            if(len(nodes_in_area1) < 1):
                break
            '''

            agent.set_starting_node(self.random_node_from_list_and_pop(self.free_node_list))
            agent.set_target_node(self.random_node_from_list(area.node_list))

            agent.randomize_velocity()
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1

        print('homing agents created {}'.format(number))
        self.agent_count += number



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
        #data = dict()
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

        #data['iterations'] = it_list

        with open('agents.json', 'w') as f:
            json.dump(it_list, f, indent = 2)
        print('Simulation complete, {} steps'.format(time))

    ## TODO: move agents' tests into other class
    def do_agent_tests(self):
        agent_tester = Agent_test(self.agent_list[0])
        #agent_tester.print_street_size()
        agent_tester.print_forces()
