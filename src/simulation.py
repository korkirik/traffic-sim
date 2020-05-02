from map import *
from agent import *
from node import *
import numpy as np
import random

class Simulation:
    def __init__(self):
        self.agentCount = 0
        self.agent_id = 0

        self.v_max = 0.1
        self.headingError = 0.05
        self.agentRange = 1

        self.agentList = list()

    def load_nodes(self, recievedList):
        self.node_list = recievedList


    def create_roaming_agents(self, number):
        for i in range(number):
            agent = Agent(self.agent_id)
            agent.set_starting_node(self.node_list[i])
            agent.set_v_max(self.v_max + random.randrange(0,10,1)*0.01)
            self.agentList.append(agent)

            self.agent_id +=1
        self.agentCount += number

    # TODO: remove method
    def select_random_node(self):
        randrange(0,101,1)

    def start_simulation(self, time):
        self.iterMax = time
        agentsDataArray = np.zeros((self.iterMax*len(self.agentList),4))

        for iter in range(0, self.iterMax, 1):
            #self.findRepulsion()
            for agentIndex, agent in enumerate(self.agentList):
                agentsDataArray[agentIndex + self.agentCount*iter,0] = iter
                agentsDataArray[agentIndex + self.agentCount*iter,1] = agent.agent_id
                agentsDataArray[agentIndex + self.agentCount*iter,2] = agent.position.x
                agentsDataArray[agentIndex + self.agentCount*iter,3] = agent.position.y
                agent.updateVelocity()
                agent.updatePosition()

        np.savetxt("agentsFile.csv", agentsDataArray, delimiter=", ", header="iteration, agent_id, X, Y")
        print('Simulation complete, {} steps'.format(time))

    def findRepulsion(self):
        for agentIndex, agent in enumerate(self.agentList):
            agent.agentsInRange = 0
            for agentIndex2, agent2 in enumerate(self.agentList):
                if(agentIndex != agentIndex2):
                    #check if two agents are close
                    distance = agent.position.distanceBetween(agent2.position)
                    if(distance > self.agentRange):
                        continue

                    #check if two agents are heading to the same node
                    if(agent.nodeTo != agent2.nodeTo):
                        continue

                    #check if two agents are coming from the same node    ## WARNING: may cause unintended skipping
                    if(agent.node_out != agent2.node_out):
                        continue

                    #probably is not required
                    '''#check if two agents have the same heading vector
                    codirectionalityVector = Pvector(agent.heading.x - agent2.heading.x, agent.heading.y - agent2.heading.y)
                    if(not (math.fabs(codirectionalityVector.x) < self.headingError and math.fabs(codirectionalityVector.y) < self.headingError)):
                        continue'''

                    agent.agentsInRange += 1

                    #directional vector from agent 2 tovards agent 1
                    deltaVector = Pvector(0,0)
                    deltaVector = agent.position.subtract(agent2.position)

                    deltaVector.normalize()
                    #check if agent is behind or in front of the agent2

                    if(deltaVector.dotProduct(agent.heading)>0):
                        continue
                    else:
                        agent.slowDown()
                    #deltaVector.divideSelfByScalar(10)
                    #a = Pvector(0,0)
                    #print(deltaVector.magnitude())
                    #a = a.add(deltaVector)

                    #agent.acceleration.addToSelf(a)
            if(agent.agentsInRange == 0): #TODO slowly accelerate till v_max
                agent.velocity.setMagnitude(agent.v_max)
