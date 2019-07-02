from pvector import *
class Node:
    def __init__(self, x, y, nodeId):
        self.position = Pvector(x,y)
        self.nodeId = nodeId
        self.connectedStreetSegments = list()
        self.connectedNodesId = list()
