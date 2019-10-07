from pvector import *
from node import *
import random

class Agent:
                                        #do we need start Node? -K
    def __init__(self, x, y, vMax, agentId, startNode): # , goal):

        #self.x = float(x)
        #self.y = float(y)
        self.vMax = float(vMax)
        self.agentId = agentId
        self.position = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.approachError = 0.2
        #self.goal = node(0,0,0)

        self.nodeOut = startNode
        self.position = startNode.position

        self.delta_r = Pvector(0,0)
        self.pickNode()

    def pickNode(self):
        print('I am at Node ', self.nodeOut.nodeId)
        pickedNode = random.randint(0,len(self.nodeOut.connectedNodes)-1)  #pick random N0de from available

        #print('picked node', pickedNode, 'out of ',len(self.nodeOut.connectedNodes) )

        self.nodeTo = self.nodeOut.connectedNodes[pickedNode]
    #    for obj in self.nodeOut.connectedNodes:
    #        print('adjacent nodes ', obj.nodeId)
    #    print('Going to ', self.nodeTo.nodeId)
    #    print('k')
        #for nodeTo in self.nodeTo.connectedNodes:
            #print('node T', nodeTo.nodeId)

        nextNode_vector = Pvector(self.nodeTo.position.x, self.nodeTo.position.y) #directional vector towards next node
        nextNode_vector.subtractFromSelf(self.position) #heading of the agent

        #self.delta_r = self.delta_r.add(nextNode_vector)

        self.distanceToNextNode = nextNode_vector.magnitude()
        nextNode_vector.normalize()
        nextNode_vector.setMagnitude = self.vMax
        self.velocity = nextNode_vector

    def updateVelocity(self):
        self.velocity = self.velocity.add(self.acceleration)

    def updatePosition(self):
        self.position = self.position.add(self.velocity)
        self.distanceToNextNode = self.distanceToNextNode - self.vMax #currently move with vMax, should change to magnitude of current speed
        #self.delta_r = self.delta_r.subtract(self.velocity)
        if(self.distanceToNextNode < self.approachError):
                self.nodeOut = self.nodeTo
                self.pickNode()




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
