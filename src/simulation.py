from map import *
from agent import *
from node import *

#from agentcontroller import *

class Simulation:
    def __init__(self):
        self.agentCount = 0
        self.agentID = 1
        self.vMax = 1
        self.agentList = list()

    def loadNodes(self, recievedList):
        self.nodeList = recievedList


    def createRoamingAgents(self, number):
        self.agentList.append(Agent(0, 0, self.vMax, self.agentID, self.nodeList[2]))
        self.agentCount += number

    def startSimulation(self, time):
        self.iterMax = time

        for iter in range(0, self.iterMax):
            for agent in self.agentList:
                agent.updateVelocity()
                agent.updatePosition()
                print(agent.position.x, agent.position.y)
    #obsolete
    #def agentsOnMap(map,agentController):
    #agent = placeAgents(agentController)
    #Run agents on map
    #map1 = drawMap(map)
    #def drawMap(map):
    #    map = map.drawStreets()
    #    return map
    #def placeAgents(agentController):
    #
    #    agent = agentController()
    #
    #    return agent
