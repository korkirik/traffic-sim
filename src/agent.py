#Simple agent

from pvector import *

class Agent:
                                        #do we need start Node? -K
    def __init__(self, x, y, vMax, agentId, startNode, goal):

        self.x = float(x)
        self.y = float(y)
        self.vMax = float(vMax)
        self.agentId = agentId

        self.position = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.goal = node(0,0,0)

        self.nodeFrom = startNode

    def pickNode(self):
        self.nodeTowards = self.nodeFrom.connectedNodes[1] #pick the first one
        n_vector = Pvector(self.nodeTowards.position.x, self.nodeTowards.position.y) #directional vector towards next node
        n_vector.subtractFromSelf(self.nodeFrom.position.x, self.nodeFrom.position.y)
        self.distance = n_vector.magnitude()
        n_vector.normalize()

    def moveK(self):
        pvector.addToSelf(n_vector.position.x,n_vector.position.y) # should be * V

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
