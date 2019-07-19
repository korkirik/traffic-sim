from pvector import *
class Node:
    def __init__(self, x, y, nodeId):
        self.position = Pvector(x,y)
        self.nodeId = nodeId
        self.connectedNodesId = list()
        self.connectedNodes = list()

    def removeNodeWithId(self, index_to_delete):
        for obj in self.connectedNodes:
            if(obj.nodeId == index_to_delete):
                self.connectedNodes.remove(obj)
                #remove ID
                break
