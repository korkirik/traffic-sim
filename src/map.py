from streetsegment import *
from node import *
from pvector import *
from bokeh.plotting import figure, output_file, show
output_file("map_build_0.0.1.html")

class Map:
    def __init__(self):
        self.name = 'defaultMapName'
        self.nodeList = list()

    def loadStreets(self, recievedList):
        self.streetSegmentList = recievedList.copy()
        length = len(self.streetSegmentList)
        for index in range(0,length,1):
            print(self.streetSegmentList[index].startPoint.x, self.streetSegmentList[index].startPoint.y,
                self.streetSegmentList[index].endPoint.x, self.streetSegmentList[index].endPoint.y)

    def generateNodes(self):
        length = len(self.streetSegmentList)
        self.nodeCounter = 0
        for index in range(0,length,1):
            self.nodeList.append(Node(self.streetSegmentList[index].startPoint.x,
                self.streetSegmentList[index].startPoint.y, self.nodeCounter))
            self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[index].name)
            self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[index].streetId)
            self.nodeCounter += 1

            self.nodeList.append(Node(self.streetSegmentList[index].endPoint.x,
                self.streetSegmentList[index].endPoint.y, self.nodeCounter))
            self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[index].name)
            self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[index].streetId)
            self.nodeCounter += 1

    def mergeNodes(self):
        for i in self.nodeList:
            '''for j in self.nodeList:
                if(i !=j):
                    if(self.nodeList[i].position.x == self.nodeList[j].position.x):
                        if(self.nodeList[i].position.y == self.nodeList[j].position.y):
                            self.nodeList[i].connectedStreetSegments.append(self.nodeList[j].connectedStreetSegments)
                            self.nodeList[i].connectedStreetSegmentsIds.append(self.nodeList[j].connectedStreetSegmentsIds)
                            self.nodeList.pop(j)'''

    def printNodesStats(self):
        print(self.nodeCounter)
        nodesNumber = len(self.nodeList)
        for index in range(0,nodesNumber, 1):
            print(self.nodeList[index].position.x, self.nodeList[index].position.y, self.nodeList[index].nodeId)

    def drawStreets(self):
        p = figure(plot_width=700, plot_height=700)
        length = len(self.streetSegmentList)
        for index in range(0,length,1):
            x = [self.streetSegmentList[index].startPoint.x, self.streetSegmentList[index].endPoint.x]
            y = [self.streetSegmentList[index].startPoint.y,self.streetSegmentList[index].endPoint.y]
            p.line(x, y, line_width=2)

        nodesNumber = len(self.nodeList)
        for index in range(0,nodesNumber, 1):
            x = self.nodeList[index].position.x
            y = self.nodeList[index].position.y
            p.circle(x, y, fill_color="white", size=8)
        show(p)
