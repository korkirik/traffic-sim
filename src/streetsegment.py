from pvector import Pvector

class StreetSegment:
    def __init__(self, start_point, end_point):
        self.start_point = start_point #Points are pvectors
        self.end_point = end_point
        #defaults
        #self.name = 'defaultName'
        #self.lanes = 1          # TODO: Not used, remove or implement something
        #self.lanesForward = 1   # TODO: Not used, remove or implement something
        #self.lanesBackward = 1  # TODO: Not used, remove or implement something
        #self.streetType = 'street' # TODO: Not used, remove or implement something
        #self.streetId = 0
        #self.speed = 50         # TODO: Not used, remove or implement something

    @property
    def length(self):
        delta_r = self.end_point - self.start_point
        return delta_r.magnitude()
