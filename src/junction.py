'''
 * Classname
 *  - Junction
 *
 * Brief
 *  - A class that resembles a crossroad in the map.
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A Junction is like a crossroad in the real world, ususally is
 *    the place where 4 streets come across. One junction contains
 *    basically 8 junction points, from which each pair represents
 *    driving "in" and "out" of the street.
'''

class Junction:

    def __init__(self, xCoordinate, yCoordinate):
        x = float(xCoordinate)
        y = float(yCoordinate)
        self.junLocation = Pvector(x,y) # Where the center of the junction is located
        self.subJunctions = list() # A vector of 8 junction points at one crossroad, including 4 in and 4 out
        self.addPoints(x,y)
        self.setStatus()

    #Add points to the junction
    # 8 junction points will be added by calling it once

    # something TODO about this method
    def addPoints(self, xCoordinate, yCoordinate):
        x = float(xCoordinate)
        y = float(yCoordinate)
        self.subJunctions.append(JunctionPoint(x+20,y-10,0))
        self.subJunctions.append(JunctionPoint(x+10,y-20,1))
        self.subJunctions.append(JunctionPoint(x-10,y-20,2))
        self.subJunctions.append(JunctionPoint(x-20,y-10,3))
        self.subJunctions.append(JunctionPoint(x-20,y+10,4))
        self.subJunctions.append(JunctionPoint(x-10,y+20,5))
        self.subJunctions.append(JunctionPoint(x+10,y+20,6))
        self.subJunctions.append(JunctionPoint(x+20,y+10,7))

    #Filter out the points where no further connection is possible,
    # and set up "in" and "out" points
    def setStatus(self):
        length = len(self.subJunctions)
        for i in range(0,length,2):
                self.subJunctions[i].inOrOut = 0
        for i in range(1,length,2):
                self.subJunctions[i].inOrOut = 1
        for i in self.subJunctions:
            if self.subJunctions[i].x > 410 || self.subJunctions[i].x <-410:
                self.subJunctions[i].accessible = false
            elif self.subJunctions[i].y > 410 || self.subJunctions[i].y <-410:
                self.subJunctions[i].accessible = false
