#Brief Rewritten and Refactored from code in C
#  - A toolbox that manipulate all the physics behind the simulation
# Detail
# - Pvector class contains all the necessary tools for doing maths
#   on a two-dimensional vector space. Most of the functions here
#   to generate ideal forces to drive the agents.
import math

class Pvector:

    def __init__(self, xCoordinate, yCoordinate):
        self.x = 0
        self.y = 0
        if(xCoordinate != 0):
            self.x = float(xCoordinate)
        if(yCoordinate != 0):
            self.y = float(yCoordinate)

    def add(self, vector):
        x = self.x + vector.x
        y = self.y + vector.y
        return Pvector(x, y)

    def subtract(self, vector):
        x1 = self.x - vector.x
        y1 = self.y - vector.y
        return Pvector(x1, y1)

    def multiply(self, alpha):
        x = self.x * alpha
        y = self.y * alpha
        return Pvector(x, y)

    def divide(self, alpha):
        if alpha != 0:
            x = self.x/float(alpha)
            y = self.y/float(alpha)
            return Pvector(x, y)
        else:
            return Pvector(self.x, self.y)
            print('Division by zero')

    def addToSelf(self, vector):
        self.x = self.x + vector.x
        self.y = self.y + vector.y

    def subtractFromSelf(self, vector):
        self.x = self.x - vector.x
        self.y = self.y - vector.y

    def multiplySelfByScalar(self, alpha):
        self.x = self.x * alpha
        self.y = self.y * alpha

    def divideSelfByScalar(self, alpha):
        if alpha != 0:
            self.x = self.x/float(alpha)
            self.y = self.y/float(alpha)
        else:
            print('Division by zero')

    def magnitudeSquared(self):
        return self.x*self.x + self.y*self.y

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        mag = self.magnitude()
        self.divideSelfByScalar(mag)

    def get(self):
        return self

    def copy(self):
        return Pvector(self.x, self.y)

    def setMagnitude(self, x):
        self.normalize()
        self.multiplySelfByScalar(x)

    def limitMagnitude(self, lim):
        if self.magnitude() > lim:
            self.setMagnitude(lim)

    def dotProduct(self, vector):
        x = self.x * vector.x
        y = self.y * vector.y
        return x + y

    #TODO swap for atan2 for a safer angle determination
    def angleBetween(self, vector):
        angle = math.acosf(self.dotProduct(vector)/(self.magnitude() * vector.magnitude()))
        return angle

    def distanceBetween(self, vector):
        return math.sqrt((self.x - vector.x)*(self.x - vector.x) + (self.y - vector.y)*(self.y - vector.y))

    def getNormalPoint(self, b, p):
        pa = p.subtract(self)
        ba = b.subtract(self)
        ba.normalize()
        value = pa.dotProduct(ba)
        ba.multiplySelfByScalar(value)
        normalPoint = a.add(ba)
        return normalPoint

    def whoAmI(self):
        print('vector', self.x, self.y)

    @classmethod
    def dot_product(self, vector1, vector2):
        x = vector1.x * vector2.x
        y = vector1.y * vector2.y
        return x + y
