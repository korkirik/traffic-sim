from map import *
from agent import *
from node import *
import numpy as np
import random

class Simulation:
    def __init__(self):
        self.agent_count = 0
        self.agent_id = 0

        self.v_max = 0.1
        self.heading_error = 0.05

        self.agent_list = list()

    def load_nodes(self, recievedList):
        self.node_list = recievedList


    def create_roaming_agents(self, number):
        for i in range(number):
            agent = Agent(self.agent_id)
            agent.set_starting_node(self.node_list[i])
            agent.set_v_max(self.v_max + random.randrange(0,10,1)*0.01)
            self.agent_list.append(agent)
            agent.add_agent_list(self.agent_list)

            self.agent_id +=1
        self.agent_count += number
        #for agent in self.agent_list:
        #    print(len(agent.agent_list))

    def start_simulation(self, time):
        self.iterMax = time
        agentsDataArray = np.zeros((self.iterMax*len(self.agent_list),4))

        for iter in range(0, self.iterMax, 1):
            #self.findRepulsion()
            for agentIndex, agent in enumerate(self.agent_list):
                agentsDataArray[agentIndex + self.agent_count*iter,0] = iter
                agentsDataArray[agentIndex + self.agent_count*iter,1] = agent.agent_id
                agentsDataArray[agentIndex + self.agent_count*iter,2] = agent.position.x
                agentsDataArray[agentIndex + self.agent_count*iter,3] = agent.position.y
                agent.update_behaviour()
                agent.update_velocity()
                agent.update_position()

        np.savetxt("agentsFile.csv", agentsDataArray, delimiter=", ", header="iteration, agent_id, X, Y")
        print('Simulation complete, {} steps'.format(time))
        #print('data saved in agentsFile.csv')
