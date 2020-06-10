from map import *
from agent import *
from homing_agent import *
from node import *
import numpy as np
import random

class Simulation:
    def __init__(self):
        self.agent_count = 0
        self.agent_id = 0

        self.agent_list = list()

    def load_nodes(self, recievedList):
        self.node_list = recievedList

    def create_roaming_agents(self, number):
        for i in range(number):
            agent = Agent(self.agent_id)

            agent.set_starting_node(self.random_node())
            agent.randomize_velocity()
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number

    def create_hoaming_agents(self, number):
        #nodes_in_area1 = self.nodes_area_select(6.11, 51.7805, 0.002)
        #nodes_in_area2 = self.nodes_area_select(6.1255, 51.782, 0.001)
        #print(len(nodes_in_area1))
        #print(len(nodes_in_area2))
        for i in range(number):
            agent = HomingAgent(self.agent_id)
            agent.set_starting_node(self.node_list[i])
            agent.set_target_node(self.node_list[3]) # self.node_list[100]

            #agent.set_starting_node(self.random_node_from_list(nodes_in_area1))
            #agent.set_target_node(self.random_node_from_list(nodes_in_area2))

            #agent.randomize_velocity()
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number

    def random_node(self):
        l = len(self.node_list)
        node = self.node_list[random.randrange(0,l,1)]
        return node

    def random_node_from_list(self,list_):
        l = len(list_)
        node = list_[random.randrange(0,l,1)]
        return node

    def nodes_area_select(self, x, y, radius):
        selected_nodes = list()
        center = Pvector(x,y)

        for node in self.node_list:
            distance_vector = node.position - center
            distance = distance_vector.magnitude()
            if(distance <= radius):
                selected_nodes.append(node)

        return selected_nodes




    def start_simulation(self, time):
        self.iterMax = time
        agentsDataArray = np.zeros((self.iterMax*len(self.agent_list),4))

        for iter in range(0, self.iterMax, 1):

            for agentIndex, agent in enumerate(self.agent_list):
                agentsDataArray[agentIndex + self.agent_count*iter,0] = iter
                agentsDataArray[agentIndex + self.agent_count*iter,1] = agent.agent_id
                agentsDataArray[agentIndex + self.agent_count*iter,2] = agent.position.x
                agentsDataArray[agentIndex + self.agent_count*iter,3] = agent.position.y
                agent.update_behaviour()
                agent.update_velocity()
                agent.update_position()

                #self.do_agent_tests()

        np.savetxt("agentsFile.csv", agentsDataArray, delimiter=", ", header="iteration, agent_id, X, Y")
        print('Simulation complete, {} steps'.format(time))
        #print('data saved in agentsFile.csv')

    ## TODO: move agents' tests into other class
    def do_agent_tests(self):
        agent_tester = Agent_test(self.agent_list[0])
        #agent_tester.print_street_size()
        agent_tester.print_forces()
