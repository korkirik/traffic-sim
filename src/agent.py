from pvector import *
from node import *
import random

class Agent:
                                        #do we need start Node? -K
    def __init__(self, x, y, vMax, agentId, startNode): # , goal):

        self.position = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.agentId = agentId


        self.vMax = vMax
        self.breakRate = vMax/10


        self.approachError = 0.2
        self.agentsInRange = 0
        #self.goal = node(0,0,0)
        self.heading = Pvector(0,0)

        self.nodeOut = startNode
        self.position = startNode.position

        self.delta_r = Pvector(0,0)
        
        self.pickNode()

    def pickNode(self):
        print(self.agentId,' at ', self.nodeOut.nodeId)
        pickedNode = random.randint(0,len(self.nodeOut.connectedNodes)-1)  #pick random N0de from available
        #print('picked node', pickedNode, 'out of ',len(self.nodeOut.connectedNodes) )

        self.nodeTo = self.nodeOut.connectedNodes[pickedNode]
        self.updateDistanceHeading()
        self.velocity = self.heading.multiply(self.vMax)

    def updateDistanceHeading(self):
        vectorToNextNode = Pvector(self.nodeTo.position.x, self.nodeTo.position.y)
        vectorToNextNode.subtractFromSelf(self.position)
        self.distanceToNextNode = vectorToNextNode.magnitude()
        vectorToNextNode.normalize()
        self.heading = vectorToNextNode.returnCopy()


    def projectAcceleration(self):
        dotProduct = self.acceleration.dotProduct(self.heading)
        self.acceleration = self.heading.multiply(dotProduct)

    def updateVelocity(self):
        #self.projectAcceleration() #why
        self.velocity = self.velocity.add(self.acceleration)

    def updatePosition(self):
        self.position = self.position.add(self.velocity)
        self.updateDistanceHeading()
        a = Pvector.dotProductCM(self.velocity, self.heading)
        if(a < 0):
            if(self.distanceToNextNode < self.approachError):
                self.nodeOut = self.nodeTo
                self.pickNode()

    #def detectAgentsAround(self):
        #calculate resulting force

    def printNodesIsee(self):
        print('start connections:')
        for obj in self.nodeOut.connectedNodes:
            print(obj.nodeId)

        print('next connections:')
        for n in self.nodeTo.connectedNodes:
            print(n.nodeId)


    def slowDown(self):
        #self.acceleration = self.heading.multiply(-1*self.breakRate) #TODO change to sum later
        self.velocity = self.velocity.subtract(self.heading.multiply(self.breakRate))
        if(self.velocity.magnitude() < 0):
            self.velocity.multiplySelfByScalar(0)
