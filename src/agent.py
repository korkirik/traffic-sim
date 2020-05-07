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
        self.alpha = 2
        self.break_rate = 0.01

        self.separation = 1
        self.approach_error = 0.2
        self.agent_range = 1
        self.agents_in_range = 0
        self.heading = Pvector(0,0)
        self.delta_r = Pvector(0,0)
#--------------setters-------------------
    def set_starting_node(self, start_node):
        self.node_out = start_node
        self.position = start_node.position
        self.pick_node()

    def set_v_max(self, v_max):
        self.v_max = v_max

    def add_agent_list(self, agent_list):
        self.agent_list = agent_list

#-------------Main Logic-----------------
    ## TODO: Gather all behaviours here
    def update_behaviour(self):
        self.next_node_attraction()
        self.feel_repulsion()

    def update_velocity(self):
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit_magnitude(self.v_max)

    def update_position(self):
        self.position = self.position + self.velocity
        self.update_distance_heading_towards_next_node()
        #a = Pvector.dot_product(self.velocity, self.heading)
        #if(a < 0):
        if(self.distance_to_next_node < self.approach_error):
            self.node_out = self.nodeTo
            self.pick_node()
#-----------------------------------------
    def print_reachable_nodes(self):
        print('start connections:')
        for obj in self.node_out.connected_nodes:
            print(obj.node_id)

        print('next connections:')
        for n in self.nodeTo.connected_nodes:
            print(n.node_id)
#-------------Behaviours------------------
    def pick_node(self):
        #print(self.agent_id,' at ', self.node_out.node_id)
        picked_node = random.randint(0,len(self.node_out.connected_nodes)-1)  #pick random N0de from available
        #print('picked node', picked_node, 'out of ',len(self.node_out.connected_nodes) )

        self.nodeTo = self.node_out.connected_nodes[picked_node]
        self.update_distance_heading_towards_next_node()
        #self.velocity = self.heading.multiply(self.v_max)

    def update_distance_heading_towards_next_node(self):
        vector_to_next_node = Pvector(self.nodeTo.position.x, self.nodeTo.position.y)
        vector_to_next_node = vector_to_next_node - self.position
        self.distance_to_next_node = vector_to_next_node.magnitude()
        vector_to_next_node.normalize()
        self.heading = vector_to_next_node.copy()

    def next_node_attraction(self):
        self.acceleration = self.acceleration + self.heading.multiply(self.alpha)

    def slow_down(self):
        #self.acceleration = self.heading.multiply(-1*self.break_rate) #TODO change to sum later
        self.velocity.divide_itself(2)
        #self.velocity = self.velocity - self.heading.multiply(self.break_rate)
        #if(self.velocity.magnitude() < 0):## TODO: magnitude can not be negative, fix
            #self.velocity.multiply_itself(0)

    def feel_repulsion(self):
        self.agents_in_range = 0
        for agent_index, agent in enumerate(self.agent_list):
            if(agent != self):
                #check if two agents are close
                distance = Pvector.distance_between(agent.position, self.position)
                if(distance > self.agent_range):
                    continue

                #check if two agents are heading to the same node
                if(self.nodeTo != agent.nodeTo):
                    continue

                #check if two agents are coming from the same node    ## WARNING: may cause unintended skipping
                if(self.node_out != agent.node_out):
                    continue
                self.agents_in_range += 1

                #directional vector from this agent tovards the agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - self.position

                delta_vector.normalize()

                #check if the agent is behind or in front
                if(Pvector.dot_product(delta_vector, self.heading) < 0):
                    continue
                else:
                    self.slow_down()
                #delta_vector.divide_itself(10)
                #a = Pvector(0,0)
                #print(delta_vector.magnitude())
                #a = a.add(delta_vector)

                #agent.acceleration + a
    #    if(self.agents_in_range == 0): #TODO slowly accelerate till v_max
    #        self.velocity.set_magnitude(self.v_max)
