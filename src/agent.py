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
        self.agent_range = 1
        self.agents_in_range = 0
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
        vector_to_next_node = Pvector(self.nodeTo.position.x, self.nodeTo.position.y)
        vector_to_next_node = vector_to_next_node - self.position
        self.distance_to_next_node = vector_to_next_node.magnitude()
        vector_to_next_node.normalize()
        self.heading = vector_to_next_node.copy()

    def set_starting_node(self, start_node):
        self.node_out = start_node
        self.position = start_node.position
        self.pick_node()

    def set_v_max(self, v_max):
        self.v_max = v_max

        ## TODO: make it work
    def projectAcceleration(self):
        dot_product = Pvector.dot_product(self.acceleration, self.heading)
        self.acceleration = self.heading.multiply(dot_product)

    ## TODO: Gather all behaviours here
    def update_behaviour(self):
        self.feel_repulsion()

    def update_velocity(self):
        #self.projectAcceleration() ## TODO: fix
        self.velocity = self.velocity + self.acceleration

    def update_position(self):
        self.position = self.position + self.velocity
        self.update_distance_heading()
        #a = Pvector.dot_product(self.velocity, self.heading)
        #if(a < 0):
        if(self.distance_to_next_node < self.approachError):
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
        self.velocity = self.velocity - self.heading.multiply(self.breakRate)
        if(self.velocity.magnitude() < 0):## TODO: magnitude can not be negative, fix
            self.velocity.multiplySelfByScalar(0)

    def add_agent_list(self, agent_list):
        self.agent_list = agent_list

    def feel_repulsion(self):
        for agent_index, agent_nearby in enumerate(self.agent_list):
            self.agents_in_range = 0
            if(self != agent_nearby):
                #check if two agents are close
                distance = Pvector.distance_between(self.position, agent_nearby.position)
                if(distance > self.agent_range):
                    continue

                #check if two agents are heading to the same node
                if(self.nodeTo != agent_nearby.nodeTo):
                    continue

                #check if two agents are coming from the same node    ## WARNING: may cause unintended skipping
                if(self.node_out != agent_nearby.node_out):
                    continue

                self.agents_in_range += 1

                #directional vector from this agent tovards the agent_nearby
                delta_vector = Pvector(0,0)
                delta_vector = agent_nearby.position - self.position

                delta_vector.normalize()

                #check if the agent_nearby is behind or in front
                if(Pvector.dot_product(delta_vector, agent_nearby.heading) > 0):
                    continue
                else:
                    self.slowDown()
                #delta_vector.divideSelfByScalar(10)
                #a = Pvector(0,0)
                #print(delta_vector.magnitude())
                #a = a.add(delta_vector)

                #agent.acceleration.addToSelf(a)
        if(self.agents_in_range == 0): #TODO slowly accelerate till v_max
            self.velocity.setMagnitude(self.v_max)
