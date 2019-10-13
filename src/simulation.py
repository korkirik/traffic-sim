from map import *
from agent import *
from node import *
import numpy as np

class Simulation:
    def __init__(self):
        self.agentCount = 0
        self.agentId = 1
        self.vMax = 1
        self.agentList = list()

    def loadNodes(self, recievedList):
        self.nodeList = recievedList


    def createRoamingAgents(self, number):
        self.agentList.append(Agent(0, 0, self.vMax, self.agentId, self.nodeList[0]))
        self.agentCount += number

    def startSimulation(self, time):
        self.iterMax = time
        agentsDataArray = np.zeros((self.iterMax*len(self.agentList),4))

        for iter in range(0, self.iterMax, 1):
            for agentIndex, agent in enumerate(self.agentList):
                agentsDataArray[agentIndex + self.agentCount*iter,0] = iter
                agentsDataArray[agentIndex + self.agentCount*iter,1] = agent.agentId
                agentsDataArray[agentIndex + self.agentCount*iter,2] = agent.position.x
                agentsDataArray[agentIndex + self.agentCount*iter,3] = agent.position.y
                agent.updateVelocity()
                agent.updatePosition()

        np.savetxt("agentsFile.csv", agentsDataArray, delimiter=", ", header="iteration, agentId, X, Y")
