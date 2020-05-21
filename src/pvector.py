#Brief Rewritten and Refactored from code in C
#  - A toolbox that manipulate all the physics behind the simulation
# Detail
# - Pvector class contains all the necessary tools for doing maths
#   on a two-dimensional vector space. Most of the functions here
#   to generate ideal forces to drive the agents.
import math

class Pvector:

    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        if(x != 0):
            self.x = float(x)
        if(y != 0):
            self.y = float(y)

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

    def multiply_itself(self, alpha):
        self.x = self.x * alpha
        self.y = self.y * alpha

    def divide_itself(self, alpha):
        if alpha != 0:
            self.x = self.x/float(alpha)
            self.y = self.y/float(alpha)
        else:
            print('Division by zero')

    def magnitude_squared(self):
        return self.x*self.x + self.y*self.y

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        mag = self.magnitude()
        self.divide_itself(mag)

    def copy(self):
        return Pvector(self.x, self.y)

    def set_magnitude(self, x):
        self.normalize()
        self.multiply_itself(x)

    def limit_magnitude(self, lim):
        if self.magnitude() > lim:
            self.set_magnitude(lim)

    def smooth_limit_magnitude(self, lim):
        pass
        #if self.magnitude() > lim:
            #self.set_magnitude(lim)
    @staticmethod
    def check_zero_magnitude(one):
        if one.x == one.y and one.x == 0:
            print('Zero length vector')

    @staticmethod
    def turn_vector(direction, vector):
        direction.set_magnitude(vector.magnitude())
        return direction

    @staticmethod
    def angle_between(one, other):
        cosine = Pvector.dot_product(one, other)/( one.magnitude() * other.magnitude() )
        c_magnitude = Pvector.cross_product_magnitude(one, other)
        sine = c_magnitude / ( one.magnitude() * other.magnitude() )
        angle = math.atan2(sine,cosine)
        return angle *360 /(2* math.pi)

    @staticmethod #for 2D vectors
    def cross_product_magnitude(one, other):
        return one.x * other.y - one.y * other.x

    @staticmethod
    def distance_between_points(one, other):
        return math.sqrt((one.x - other.x)*(one.x - other.x) + (one.y - other.y)*(one.y - other.y))

    @staticmethod
    def get_normal_point(one, other):
        pass

    @staticmethod
    def dot_product(one, other):
        x = one.x * other.x
        y = one.y * other.y
        return x + y

    def show(self):
        print('vector {},{}'.format(self.x, self.y))
