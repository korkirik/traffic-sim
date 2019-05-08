#include "path.h"

from Destinations import *
from Pvector import *
from Junction import *

x = 0
x = float(x)
y = 0
y = float(y)

def Path():

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

    Destinations.push_back(Pvector( 380, 380))
    Destinations.push_back(Pvector( 120,-380))
    Destinations.push_back(Pvector(-320, 220))
    Destinations.push_back(Pvector(  80,  20))


def addMainJunctions(x, y):

    mainJunctions.push_back(Junction(x,y))

