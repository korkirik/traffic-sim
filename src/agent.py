from pvector import *
from node import *
import random

class Agent:

    def __init__(self, agent_id):

        self.position = Pvector(0,0)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.agent_id = agent_id

        self.v_max = 0.00002
        self.alpha = 0.00001 # v_max/2
        self.beta =  0.000008 #0.8 * alpha
        self.decceleration_magnitude = 0

        #self.minimal_separation = 0.00075 #75 *self.alpha
        self.approach_error = 0.00002 # 0.2 * self.alpha
        self.agent_range = 0.0001 # 10 *self.alpha
        self.agents_in_range = 0
        self.heading = Pvector(0,0)
        self.distance_to_next_node = 0
        self.active = 1

        self.delta = Pvector(0,0)
#--------------setters-------------------
    def set_starting_node(self, start_node):
        self.preceding_node = None
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
        self.reset_acceleration()
        self.next_node_attraction()
        self.agents_aversion()

    def update_velocity(self):
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit_magnitude(self.v_max)


    def update_position(self):
        self.position = self.position + self.velocity
        self.update_next_node_vector()

        if(self.distance_to_next_node < self.approach_error):
            self.preceding_node = self.node_out
            self.node_out = self.node_in
            self.pick_node()
            self.update_next_node_vector()
            self.velocity = Pvector.turn_vector(self.heading, self.velocity)
#-----------------------------------------
    def print_reachable_nodes(self):
        print('start connections:')
        for obj in self.node_out.connected_nodes:
            print(obj.node_id)

        print('next connections:')
        for n in self.node_in.connected_nodes:
            print(n.node_id) ## TODO: remove
#-------------Behaviours------------------
    def pick_node(self):
        picked_number = self.random_roll()

        if(len(self.node_out.connected_nodes) != 1):
            while(self.node_out.connected_nodes[picked_number] == self.preceding_node):
                picked_number = self.random_roll()

        self.node_in = self.node_out.connected_nodes[picked_number]
        self.update_next_node_vector()

    def random_roll(self):
        number = random.randint(0,len(self.node_out.connected_nodes)-1)  #pick random Node from available
        #print('picked node #id {} ouf of {}'.format(self.node_out.connected_nodes[picked_number].node_id, len(self.node_out.connected_nodes)))
        return number

    def update_next_node_vector(self):
        vector_next_node = Pvector(self.node_in.position.x, self.node_in.position.y)
        vector_next_node = vector_next_node - self.position
        self.distance_to_next_node = vector_next_node.magnitude()
        vector_next_node.normalize()
        self.heading = vector_next_node.copy()

    def next_node_attraction(self):
        self.acceleration = self.acceleration + self.heading.multiply(self.alpha)

    def reset_acceleration(self):
        self.acceleration = Pvector(0,0)

    def set_inactive(self):
        self.active = 0

    def agents_aversion(self):
        self.agents_in_range = 0
        for agent_index, agent in enumerate(self.agent_list):
            if(agent != self):
                #check if two agents are close
                distance = Pvector.distance_between_points(agent.position, self.position)
                if(agent.active == 0):
                    continue

                if(distance > self.agent_range):
                    continue

                #check if two agents are heading to the same node
                if(self.node_in != agent.node_in):
                    continue

                #check if two agents are coming from the same node    ## WARNING: may cause unintended skipping
                if(self.node_out != agent.node_out):
                    continue
                self.agents_in_range += 1

                #directional vector from this agent tovards the agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - self.position

                #check if the agent is behind or in front
                if(Pvector.dot_product(delta_vector, self.heading) <= 0):
                    continue
                else:
                    #if(distance > self.minimal_separation):
                    #    self.follow(agent)
                    #    self.reset_acceleration()
                    #else:

                    self.avoid_obstacle(delta_vector)


    def avoid_obstacle(self, delta_vector):
        self.decceleration_magnitude = self.beta/(delta_vector.magnitude())
        self.delta = delta_vector
        #delta_vector.normalize()
        #decceleration = delta_vector.multiply(self.decceleration_magnitude)
        decceleration = self.heading.multiply(self.decceleration_magnitude)
        self.acceleration = self.acceleration - decceleration

class Agent_test:
    def __init__(self,agent):
        self.agent = agent

    def print_connections(self):
        agent.node_out.print_connections()

    def print_street_size(self):
        size = self.agent.distance_to_next_node
        print('distance: {}'.format(size))

    def print_forces(self):
        attraction = self.agent.alpha
        repulsion = self.agent.decceleration_magnitude
        delta = self.agent.delta

        print('attraction: {}, repulsion: {}, deltaX: {}'.format(attraction, repulsion,delta.x))
