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

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Pvector(x, y)

    def __sub__(self, other):
        x1 = self.x - other.x
        y1 = self.y - other.y
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

    def copy(self):
        return Pvector(self.x, self.y)

    def setMagnitude(self, x):
        self.normalize()
        self.multiplySelfByScalar(x)

    def limitMagnitude(self, lim):
        if self.magnitude() > lim:
            self.setMagnitude(lim)

    #TODO swap for atan2 for a safer angle determination
    def angleBetween(self, other):
        angle = math.acosf( Pvector.dot_product(self, other) / (self.magnitude() * other.magnitude() ))
        return angle

    @staticmethod
    def distance_between(one, other):
        return math.sqrt((one.x - other.x)*(one.x - other.x) + (one.y - other.y)*(one.y - other.y))

    def getNormalPoint(self, b, p):
        pa = p - self
        ba = b - self
        ba.normalize()
        value = Pvector.dot_product(pa,ba)
        ba.multiplySelfByScalar(value)
        normalPoint = a.add(ba)
        return normalPoint

    def whoAmI(self):
        print('vector', self.x, self.y)

    @staticmethod
    def dot_product(one, other):
        x = one.x * other.x
        y = one.y * other.y
        return x + y
