from pvector import *
from junction import *

class Map:
    def __init__(self):
        #in C Destinations is a list of Pvectors
        #that stores the coordinates of destinations
        # mainJunctions is a list of Junctions
        #that manages all the junctions
        self.destinations = list()
        #self.mainJunctions = list()
        self.streets = list()

        for j in range(-400,450,200):
            for i in range(-400,450,200):
                addMainJunctions(self, j, i)

        #destination
        self.destinations.append(Pvector( 380, 380))
    #Add junction on to the map
def addMainJunctions(self, x, y):
    self.mainJunctions.append(Junction(x,y))
