from streetsegment import *
from node import *
from pvector import *
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label

output_file("map_build_tg2.1.0.html")

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
            self.nodeCounter += 1

            self.nodeList.append(Node(
                self.streetSegmentList[street_index].endPoint.x,
                self.streetSegmentList[street_index].endPoint.y,
                self.nodeCounter))
            #self.nodeList[self.nodeCounter].connectedStreetSegments.append(self.streetSegmentList[street_index].name)

            self.nodeList[self.nodeCounter - 1].connectedNodes.append(self.nodeList[self.nodeCounter])
            self.nodeList[self.nodeCounter].connectedNodes.append(self.nodeList[self.nodeCounter - 1])

            self.nodeCounter += 1
        self.mergeNodes()

    def mergeNodes(self):
        rem = []
        for i in range(0,len(self.nodeList)-1):
            for j in range(i + 1, len(self.nodeList)):
                    if self.nodeList[i].position.x == self.nodeList[j].position.x:
                        if self.nodeList[i].position.y == self.nodeList[j].position.y:
                            self.nodeList[i].connectedNodes = self.nodeList[i].connectedNodes + self.nodeList[j].connectedNodes

                            self.nodeList[j].updateConnections(self.nodeList[i])    #updating links to new merged node
                            rem.append(self.nodeList[j].nodeId)

        self.nodesCreated = len(self.nodeList)

        mer = sorted(rem, reverse = True)
        self.nodeList.reverse()
        self.deleted = 0
        for indexes_to_delete in mer:           #removing Nodes that repeat
            for obj in self.nodeList:
                if(obj.nodeId == indexes_to_delete):
                    self.nodeList.remove(obj)
                    self.deleted += 1
                    break

    def printNodesStats(self, showNodes):
        print('Nodes initially created: ', self.nodesCreated)
        print('Nodes removed:', self.deleted)
        if(showNodes):
            for i in range(0,len(self.nodeList)):
                print('Node:', self.nodeList[i].nodeId, 'Adjacent Nodes:')
                for j in range(0,len(self.nodeList[i].connectedNodes)):
                    print(self.nodeList[i].connectedNodes[j].nodeId)

    def drawStreets(self):
        p = figure(plot_width=700, plot_height=700, match_aspect=True)
        for node in self.nodeList:
            for connected_node in node.connectedNodes: #Remove overlapping drawings
                x = [node.position.x, connected_node.position.x]
                y = [node.position.y, connected_node.position.y]
                p.line(x, y, line_width=2)

        for index in range(0,len(self.nodeList), 1):
            x = self.nodeList[index].position.x
            y = self.nodeList[index].position.y
            p.circle(x, y, fill_color="white", size=2)

        source = ColumnDataSource(data=dict(posY=[o.position.y for o in self.nodeList],
                                            posX=[o.position.x for o in self.nodeList],
                                            nodeids=[o.nodeId for o in self.nodeList
                                                    ]))
        labels = LabelSet(x='posX', y='posY', text='nodeids', level='glyph',
              x_offset=5, y_offset=5, text_font_size="10pt", text_color="#0c0c0c",
               source=source, render_mode='canvas')
        p.add_layout(labels)
        show(p)
