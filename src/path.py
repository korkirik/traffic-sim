from pvector import *
from Junction import *

class Path:
    def __init__(self):
    #in C Destinations is a list of Pvectors
    #that stores the coordinates of some destinations
    # mainJunctions is a list of Junctions
    #that manages all the junctions

    Destinations = list()
    mainJunctions = list()

    self.x = float(0) ???
    self.y = float(0) ???
    #TODO refactor into method with loop -K
    #Initial junctions (smaller map)
    addMainJunctions(-200, 200)
    addMainJunctions(   0, 200)
    addMainJunctions( 200, 200)
    addMainJunctions( 200,   0)
    addMainJunctions( 200,-200)
    addMainJunctions(   0,-200)
    addMainJunctions(-200,-200)
    addMainJunctions(-200,   0)
    addMainJunctions(   0,   0)

    #Newly added junctions (Bigger map)
    addMainJunctions(-400,-400)
    addMainJunctions(-200,-400)
    addMainJunctions(   0,-400)
    addMainJunctions( 200,-400)
    addMainJunctions( 400,-400)
    addMainJunctions( 400,-200)
    addMainJunctions( 400,   0)
    addMainJunctions( 400, 200)
    addMainJunctions(-400,-200)
    addMainJunctions(-400,   0)
    addMainJunctions(-400, 200)
    addMainJunctions(-400, 400)
    addMainJunctions(-200, 400)
    addMainJunctions(   0, 400)
    addMainJunctions( 200, 400)
    addMainJunctions( 400, 400)

    Destinations.append(Pvector( 380, 380))
    Destinations.append(Pvector( 120,-380))
    Destinations.append(Pvector(-320, 220))
    Destinations.append(Pvector(  80,  20))

    #Add junction on to the map
def addMainJunctions(self, x, y):
    mainJunctions.append(Junction(x,y))
