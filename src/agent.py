from pvector import *
from node import *
import random

class Agent:
                                        #do we need start Node? -K
    def __init__(self, x, y, vMax, agentId, startNode): # , goal):

        self.vMax = vMax
        self.agentId = agentId
        self.position = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
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

        # vector from current position to the next node
        nextNode_vector = Pvector(self.nodeTo.position.x, self.nodeTo.position.y)
        nextNode_vector.subtractFromSelf(self.position)

        #self.delta_r = self.delta_r.add(nextNode_vector)

        self.distanceToNextNode = nextNode_vector.magnitude()
        nextNode_vector.normalize()
        self.heading = Pvector(0,0)
        self.heading.addToSelf(nextNode_vector)
        nextNode_vector.multiplySelfByScalar(self.vMax)
        self.velocity = nextNode_vector

    def projectAcceleration(self):
        dotProduct = self.acceleration.dotProduct(self.heading)
        self.acceleration = self.heading.multiply(dotProduct)

    def updateVelocity(self):
        self.projectAcceleration()
        self.velocity = self.velocity.add(self.acceleration)

    def updatePosition(self):
        self.position = self.position.add(self.velocity)
        self.distanceToNextNode = self.distanceToNextNode - self.velocity.magnitude()
        #self.delta_r = self.delta_r.subtract(self.velocity)
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
        self.velocity.multiplySelfByScalar(0.5)


    def move(agent):

        movement = applyBehaviour(agent)

        acceleration = pvector.multiply(0)
        velocity = pvector.add(acceleration)
        velocity = pvector.limitMagnitude()
        position = pvector.add(velocity)

    def applyBehaviour():

        separate = pvector.distanceBetween()

        separate = pvector.multiply(1)

        separate = applyForce(separate)

        return separate

    def applyForce():

        force = Pvector.divide()
        acceleration = pvector.add(force)

'''
pswarm_main_run-5.py purpose and how it can be used for the agents
-Incorporate pswarm_main_run5

Which classes are required to inherit from?
-pVector.py
-pswarm_main_run5.py?

Setting initial and final destination.  Is it required?
-Relevant question is how to route traffic through Kleve?
-Travelling salesman problem.

Interfacing with map?  Simulation?
-Try and get agent and map to work together from Simulation.

Assign a time property for when agent starts of and then when it reaches destination.
Helps with calculating the velocity.  A screen velocity can be assigned to particles
later on so that it can be visualized.
'''
