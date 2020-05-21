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

    #    self.v_max = 0.1

        self.agent_list = list()

    def load_nodes(self, recievedList):
        self.node_list = recievedList

    def create_roaming_agents(self, number):
        for i in range(number):
            agent = Agent(self.agent_id)

            agent.set_starting_node(self.random_node())
        #    agent.set_v_max(self.v_max + random.randrange(0,10,1)*0.01)
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number

    def create_hoaming_agents(self, number):
        for i in range(number):
            agent = HomingAgent(self.agent_id)
            agent.set_starting_node(self.random_node())
            agent.set_target_node(self.node_list[100]) # TODO: randomize
            #agent.set_v_max(self.v_max + random.randrange(0,10,1)*0.01)
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number

    def random_node(self):
        l = len(self.node_list)
        node = self.node_list[random.randrange(0,l,1)]
        return node

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
