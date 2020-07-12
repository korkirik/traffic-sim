from pvector import *
from node import *
import random

class Agent:

    def __init__(self, agent_id):

        self.position = Pvector(0,0)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.agent_id = agent_id
        self.agent_type = 'default'

        self.v_max = 1 #0.00001 #0.1
        self.alpha = self.v_max/4
        self.beta =  1.15 * self.alpha #0.0001 * self.alpha
        self.decceleration_magnitude = 0

        #self.minimal_separation = 0.00075 #75 *self.alpha
        self.approach_error = 2 * self.alpha
        self.agent_range = 40 *self.v_max # 3
        self.agent_close_range = 20 * self.v_max
        self.detection_angle = 15

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

    def add_agent_list(self, agent_list):
        self.agent_list = agent_list

    def randomize_velocity(self):
        self.set_v_max(self.v_max + random.randrange(0,10,1)*0.01*self.v_max)

    def set_v_max(self, v_max):
        self.v_max = v_max
        self.reset_parameters()

    def reset_parameters(self):
        self.alpha = self.v_max/2
        self.beta =  0.8 * self.alpha

        #self.minimal_separation = 0.00075 #75 *self.alpha
        self.approach_error = 2 * self.alpha
        #self.agent_range = 10 *self.alpha # TODO: uncomment

#-------------Main Logic-----------------
    ## TODO: Gather all behaviours here
    def update_behaviour(self):
        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(self.agent_range, self.detection_angle)
        self.detect_agents_in_sector(self.agent_close_range, 90)
        self.detect_agents_rightward()

    def update_velocity(self):
        if (self.is_velocity_negative()):
            self.velocity = Pvector(0,0)
        else:
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

        if(len(self.node_out.connected_nodes) != 1):
            picked_number = self.random_roll()
            while(self.node_out.connected_nodes[picked_number] == self.preceding_node):
                picked_number = self.random_roll()
        else:
            picked_number = 0

        self.node_in = self.node_out.connected_nodes[picked_number]

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

    def detect_agents_rightward(self):
        self.agents_in_range = 0
        for agent_index, agent in enumerate(self.agent_list):

            if(agent != self):
                if(agent.active == 0):
                    continue

                #check if two agents are close
                distance = Pvector.distance_between_points(agent.position, self.position)
                if(distance > self.agent_range):
                    continue

                #check if two agents are going towards same node
                if(agent.node_in != self.node_in):
                    continue

                #directional vector from self tovards the other agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - self.position

                obstacle_rightward = 0
                on_the_same_line = 0

                #check if the agent is on your right, property of cross product z component
                #one on the right goes first
                if(Pvector.cross_product_magnitude(self.heading, delta_vector) < 0):
                    obstacle_rightward = 1
                    #self.agents_in_range += 1

                #check if both agents on the same street coming from the same node
                if(agent.node_out == self.node_out):
                    on_the_same_line = 1

                if(obstacle_rightward == 1 and not on_the_same_line):
                    self.brake(delta_vector)

    def detect_agents_in_sector(self, radius, angle):
        self.agents_in_range = 0
        for agent_index, agent in enumerate(self.agent_list):

            if(agent != self):
                if(agent.active == 0):
                    continue

                #check if two agents are close
                distance = Pvector.distance_between_points(agent.position, self.position)
                if(distance > radius):
                    continue

                #observe agents approaching vector, check angle between headings
                headings_angle = Pvector.angle_between(agent.heading, self.heading)
                if(math.fabs(headings_angle) > 135):
                    continue

                #directional vector from self tovards the other agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - self.position
                agent_angle = Pvector.angle_between(self.heading, delta_vector)
                #print('id {}, angle {}'.format(self.agent_id, agent_angle))
                if(math.fabs(agent_angle) < angle):
                    #obstacle ahead
                    self.brake(delta_vector)


    def brake(self, delta_vector):
        #constatnt brake force # TODO: gradient of brake force
        decceleration = self.heading.multiply(self.beta)
        self.acceleration = self.acceleration - decceleration

    def is_velocity_negative(self):

        v1 = self.velocity + self.acceleration
        if(Pvector.dot_product(v1, self.heading) <= 0):
            return True
        else:
            return False
            #self.reset_acceleration()


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
