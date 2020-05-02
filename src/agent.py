from pvector import *
from node import *
import random

class Agent:

    def __init__(self, agent_id):

        self.position = Pvector(0,0)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.agent_id = agent_id

        self.v_max = 0.1
        self.breakRate = 0.01

        self.separation = 1
        self.approachError = 0.2
        self.agentsInRange = 0
        self.heading = Pvector(0,0)
        self.delta_r = Pvector(0,0)

    def pick_node(self):
        #print(self.agent_id,' at ', self.node_out.nodeId)
        pickedNode = random.randint(0,len(self.node_out.connectedNodes)-1)  #pick random N0de from available
        #print('picked node', pickedNode, 'out of ',len(self.node_out.connectedNodes) )

        self.nodeTo = self.node_out.connectedNodes[pickedNode]
        self.update_distance_heading()
        self.velocity = self.heading.multiply(self.v_max)

    def update_distance_heading(self):
        vectorToNextNode = Pvector(self.nodeTo.position.x, self.nodeTo.position.y)
        vectorToNextNode.subtractFromSelf(self.position)
        self.distanceToNextNode = vectorToNextNode.magnitude()
        vectorToNextNode.normalize()
        self.heading = vectorToNextNode.copy()

    def set_starting_node(self, start_node):
        self.node_out = start_node
        self.position = start_node.position
        self.pick_node()

    def set_v_max(self, v_max):
        self.v_max = v_max

    def projectAcceleration(self):
        dotProduct = self.acceleration.dotProduct(self.heading)
        self.acceleration = self.heading.multiply(dotProduct)

    def updateVelocity(self):
        #self.projectAcceleration() #why
        self.velocity = self.velocity.add(self.acceleration)

    def updatePosition(self):
        self.position = self.position.add(self.velocity)
        self.update_distance_heading()
        a = Pvector.dot_product(self.velocity, self.heading)
        if(a < 0):
            if(self.distanceToNextNode < self.approachError):
                self.node_out = self.nodeTo
                self.pick_node()

    #def detectAgentsAround(self):
        #calculate resulting force

    def print_reachable_nodes(self):
        print('start connections:')
        for obj in self.node_out.connectedNodes:
            print(obj.nodeId)

        print('next connections:')
        for n in self.nodeTo.connectedNodes:
            print(n.nodeId)


    def slowDown(self):
        #self.acceleration = self.heading.multiply(-1*self.breakRate) #TODO change to sum later
        self.velocity = self.velocity.subtract(self.heading.multiply(self.breakRate))
        if(self.velocity.magnitude() < 0):
            self.velocity.multiplySelfByScalar(0)
