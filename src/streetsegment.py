from pvector import *

class StreetSegment:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint #Points are pvectors
        self.endPoint = endPoint
        #defaults
        self.name = 'defaultName'
        self.lanes = 1
        self.lanesForward = 1
        self.lanesBackward = 1
        self.streetType = 'street'
        self.streetId = 0
        self.speed = 50

    def directDistance(self):
        deltaVector = self.endPoint.subtract(startPoint)
        return deltaVector.magnitude()
