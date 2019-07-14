from streetsegment import *
from node import *
from pvector import *
from bokeh.plotting import figure, output_file, show
output_file("map_build_0.2.1.html")

class Map:
    def __init__(self):
        self.name = 'defaultMapName'
        self.nodeList = list()

    def loadStreets(self, recievedList):
        self.streetSegmentList = recievedList.copy()

    def generateNodes(self):
        length = len(self.streetSegmentList)
        self.nodeCounter = 0
        for street_index in range(0,length,1):
            self.nodeList.append(Node(
                self.streetSegmentList[street_index].startPoint.x,
                self.streetSegmentList[street_index].startPoint.y,
                self.nodeCounter))
            #self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[street_index].name)
            self.nodeList[self.nodeCounter].connectedNodesId.append(self.nodeCounter + 1)
            self.nodeCounter += 1

            self.nodeList.append(Node(
                self.streetSegmentList[street_index].endPoint.x,
                self.streetSegmentList[street_index].endPoint.y,
                self.nodeCounter))
            #self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[street_index].name)
            self.nodeList[self.nodeCounter].connectedNodesId.append(self.nodeCounter - 1)
            self.nodeCounter += 1

            self.nodeList[self.nodeCounter - 2].connectedNodes.append(self.nodeList[self.nodeCounter - 1])
            self.nodeList[self.nodeCounter - 1].connectedNodes.append(self.nodeList[self.nodeCounter - 2])

    def mergeNodes(self):
        rem = []
        for i in range(0,len(self.nodeList)-1):
            for j in range(i + 1, len(self.nodeList)):
                    if self.nodeList[i].position.x == self.nodeList[j].position.x:
                        if self.nodeList[i].position.y == self.nodeList[j].position.y:
                            self.nodeList[i].connectedNodesId = self.nodeList[i].connectedNodesId + self.nodeList[j].connectedNodesId
                            self.nodeList[i].connectedNodes = self.nodeList[i].connectedNodes + self.nodeList[j].connectedNodes
                            rem.append(self.nodeList[j].nodeId)

        print('Nodes')
        print(len(self.nodeList))
        mer = sorted(rem, reverse = True)
        print('Indexes found')
        print(len(mer))
        #print(self.nodeList)
        self.nodeList.reverse()
        #del self.nodeList[mer[0]]
        self.deleted = 0
        for indexes_to_delete in mer:
            for obj in self.nodeList:
                if(obj.nodeId == indexes_to_delete):

                    self.nodeList.remove(obj)
                    self.deleted += 1
                    break

        print('Objects removed')
        print(self.deleted)

    def printNodesStats(self):
        print('Nodes created:')
        print(self.nodeCounter)
        print('Current number of nodes')
        nodesNumber = len(self.nodeList)


    def drawStreets(self):
        p = figure(plot_width=700, plot_height=700)
        for node in self.nodeList:
            for connected_node in node.connectedNodes:
                x = [node.position.x, connected_node.position.x]
                y = [node.position.y, connected_node.position.y]
                p.line(x, y, line_width=2)

        nodesNumber = len(self.nodeList)
        for index in range(0,nodesNumber, 1):
            x = self.nodeList[index].position.x
            y = self.nodeList[index].position.y
            p.circle(x, y, fill_color="white", size=2)
        show(p)
