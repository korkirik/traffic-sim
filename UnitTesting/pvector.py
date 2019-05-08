#Brief Rewritten from code in C
#  - A toolbox that manipulate all the physics behind the simulation
# Inherit
#  - None
# Detail
# - Pvector class contains all the necessary tools for doing maths
#   on a two-dimensional vector space. Most of the functions here
#   to generate ideal forces to drive the agents.

class Pvector:
    x = 0.0
    y = 0.0

    def __init__(self, xCoordinate, yCoordinate):
        self.x = xCoordinate
        self.y = yCoordinate


    def add(self, pvector):
        self.x+= pvector.x
        self.y+= pvector.y
        return Pvector(self.x, self.y)

    def substract(self, pvector):
        self.x-= pvector.x
        self.y-= pvector.y
        return Pvector(self.x, self.y)

    def multiplyScalar(self, alpha):
        self.x *= alpha
        self.y *= alpha
        return Pvector(self.x, self.y)

    def divideScalar(self, alpha):
        if alpha != 0:
            self.x = self.x/alpha
            self.y = self.y/alpha
            return Pvector(self.x, self.y)
        else:
            print('Division by zero')
            Pvector(self.x, self.y)

    def magnitudeSquared(self):
        return self.x*self.x + self.y*self.y
