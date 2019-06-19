from pvector import *

class StreetSegment:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint #Points are pvectors
        self.endPoint = endPoint
        #defaults
        self.name = 'defaultName'
        self.lanesFromStart = 1
        self.lanesFromEnd = 1
        self.streetType = 'street'
        self.streetId = 0

    def directDistance(self):
        deltaVector = self.endPoint.subtract(startPoint)
        return deltaVector.magnitude()
