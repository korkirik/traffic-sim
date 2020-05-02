from pvector import *

class StreetSegment:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint #Points are pvectors
        self.endPoint = endPoint
        #defaults
        self.name = 'defaultName'
        self.lanes = 1          # TODO: Not used, remove or implement something
        self.lanesForward = 1   # TODO: Not used, remove or implement something
        self.lanesBackward = 1  # TODO: Not used, remove or implement something
        self.streetType = 'street' # TODO: Not used, remove or implement something
        self.streetId = 0
        self.speed = 50         # TODO: Not used, remove or implement something

    @property
    def length(self):
        delta_r = self.endPoint - self.startPoint
        return delta_r.magnitude()
