'''
 * Classname
 *  - Path
 *
 * Brief
 *  - A class that resembles the whole map
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A path is like the whole map where agents are travelling.
 *    A path object manages all the main junctions, and it also stores
 *    where the final destination are.
'''
from pvector import *
from junction import *

class Path:
    def __init__(self):
        #in C Destinations is a list of Pvectors
        #that stores the coordinates of some destinations
        # mainJunctions is a list of Junctions
        #that manages all the junctions
        self.destinations = list()
        self.mainJunctions = list()
        #TODO refactor into method with loop -K
        #Initial junctions (smaller map)
        addMainJunctions(self, -200, 200)
        addMainJunctions(self,   0, 200)
        addMainJunctions(self, 200, 200)
        addMainJunctions(self, 200,   0)
        addMainJunctions(self, 200,-200)
        addMainJunctions(self,   0,-200)
        addMainJunctions(self,-200,-200)
        addMainJunctions(self,-200,   0)
        addMainJunctions(self,   0,   0)
        #Newly added junctions (Bigger map)
        addMainJunctions(self,-400,-400)
        addMainJunctions(self,-200,-400)
        addMainJunctions(self,   0,-400)
        addMainJunctions(self, 200,-400)
        addMainJunctions(self, 400,-400)
        addMainJunctions(self, 400,-200)
        addMainJunctions(self, 400,   0)
        addMainJunctions(self, 400, 200)
        addMainJunctions(self,-400,-200)
        addMainJunctions(self,-400,   0)
        addMainJunctions(self,-400, 200)
        addMainJunctions(self,-400, 400)
        addMainJunctions(self,-200, 400)
        addMainJunctions(self,   0, 400)
        addMainJunctions(self, 200, 400)
        addMainJunctions(self, 400, 400)
        self.destinations.append(Pvector( 380, 380))
        self.destinations.append(Pvector( 120,-380))
        self.destinations.append(Pvector(-320, 220))
        self.destinations.append(Pvector(  80,  20))

    #Add junction on to the map
def addMainJunctions(self, x, y):
    self.mainJunctions.append(Junction(x,y))
