from pvector import *
class Node:
    def __init__(self, x, y, nodeId):
        self.position = Pvector(x,y)
        self.nodeId = nodeId
        self.connectedNodes = list()
        self.merged = False

    def removeConnectionsToMe(self):
        for obj in self.connectedNodes:
            for o in obj.connectedNodes:
                if(o.nodeId == self.nodeId):
                    obj.connectedNodes.remove(o)
                    break

    def addConnectionsToMe(self):
        for obj in self.connectedNodes:
            foundFlag = False
            for o in obj.connectedNodes:
                if(o.nodeId == self.nodeId):
                    foundFlag = True
                    break                   #found id in list
            if(not foundFlag):
                obj.connectedNodes.append(self)


    def removeConnectedNodeWithId(self, index_to_delete):
        for obj in self.connectedNodes:
            if(obj.nodeId == index_to_delete):
                self.connectedNodes.remove(obj)
                break
