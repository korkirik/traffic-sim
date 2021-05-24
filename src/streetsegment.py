from pvector import Pvector

class StreetSegment:
    def __init__(self, start_point, end_point):
        self.start_point = start_point #Points are pvectors
        self.end_point = end_point
        #defaults
        #self.name = 'defaultName'

    @property
    def length(self):
        delta_r = self.end_point - self.start_point
        return delta_r.magnitude()
