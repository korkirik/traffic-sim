from map import *
from agent import *
from agentcontroller import *

class Simulation:
    
    def agentsOnMap(map,agentController):
        
        map1 = drawMap(map)
        agent = placeAgents(agentController)
        
        #Run agents on map
    
    def drawMap(map):
        
        self.mapsLists = list()
        
    def placeAgents(agentController):
        
        agent = agentController()