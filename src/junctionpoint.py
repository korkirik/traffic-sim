'''
 * Classname
 *  - JunctionPoint
 *
 * Brief
 *  - A class that resembles driving "in" or "out" a street
 *
 * Inherit
 *  - class Pvector
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A Junction point is like the entrance or exit of the street.
 *    As this class inherits from the Pvector class, each junction
 *    points has its own coordinates. In addition, it also carries
 *    other infomation like accessibility, direction (in or out)...etc.
 *
'''
from pvector import *

class JunctionPoint(Pvector):

    def __init__(self, x, y, i):
        self.x = float(x)
        self.y = float(y)
        self.i = int(i)

        #If this junction point can take you to next junction, it's accessible.
        # Otherwise, it's not (e.g. at the corner)
        self.accessible = True
        # A street has only two ends, one is to drive in,
        #the other is to drive out
        self.inOrOut = True
        #It's used to record the relative position of the
        # junction points at the junction
        self.index = i

    #Return a junction point object
def get():
    return self #Lets try this -K
