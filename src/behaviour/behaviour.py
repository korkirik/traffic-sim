from pvector import Pvector
from node import Node

import math

class Behaviour:

    def __init__(self):
        pass

    def set_starting_node(self, start_node):
        pass

    def set_target_node(self, target_node):
        pass

    def pick_next_node(self):
        pass

    def update_behaviour(self):
        pass

    def update_velocity(self):
        pass

    def update_position(self):
        pass
#-----------Concrete Functions-----------
    def detect_agents_rightward(self):
        host = self.host

        host.agents_in_range = 0
        for agent_index, agent in enumerate(host.agent_list):

            if(agent != host):
                if(agent.active == 0):
                    continue

                #check if two agents are close
                distance = Pvector.distance_between_points(agent.position, host.position)
                if(distance > host.agent_range):
                    continue

                #check if two agents are going towards same node
                if(agent.node_in != host.node_in):
                    continue

                #directional vector from self tovards the other agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - host.position

                obstacle_rightward = 0
                on_the_same_line = 0

                #check if the agent is on your right, property of cross product z component
                #one on the right goes first
                if(Pvector.cross_product_magnitude(host.heading, delta_vector) < 0):
                    obstacle_rightward = 1
                    #self.agents_in_range += 1

                #check if both agents on the same street coming from the same node
                if(agent.node_out == host.node_out):
                    on_the_same_line = 1

                if(obstacle_rightward == 1 and not on_the_same_line):
                    self.brake(delta_vector)

    def detect_agents_in_sector(self, radius, angle):
        host = self.host

        host.agents_in_range = 0
        for agent_index, agent in enumerate(host.agent_list):

            if(agent != host):
                if(agent.active == 0):
                    continue

                #check if two agents are close
                distance = Pvector.distance_between_points(agent.position, host.position)
                if(distance > radius):
                    continue

                #observe agents approaching vector, check angle between headings
                headings_angle = Pvector.angle_between(agent.heading, host.heading)
                if(math.fabs(headings_angle) > 135):
                    continue

                #directional vector from self tovards the other agent
                delta_vector = Pvector(0,0)
                delta_vector = agent.position - host.position
                agent_angle = Pvector.angle_between(host.heading, delta_vector)
                #print('id {}, angle {}'.format(self.agent_id, agent_angle))
                if(math.fabs(agent_angle) < angle):
                    #obstacle ahead
                    self.brake(delta_vector)

    def is_velocity_negative(self):
        host = self.host
        v1 = host.velocity + host.acceleration
        if(Pvector.dot_product(v1, host.heading) <= 0):
            return True
        else:
            return False

    def reset_acceleration(self):
        self.host.acceleration = Pvector(0,0)

    def next_node_attraction(self):
        host = self.host
        host.acceleration = host.acceleration + host.heading.multiply(host.alpha)

    def update_next_node_vector(self):
        host = self.host
        vector_next_node = Pvector(host.node_in.position.x, host.node_in.position.y)
        vector_next_node = vector_next_node - host.position
        host.distance_to_next_node = vector_next_node.magnitude()
        vector_next_node.normalize()
        host.heading = vector_next_node.copy()

    def brake(self, delta_vector = Pvector(0,0)):
        #constatnt brake force # TODO: gradient of brake force
        host = self.host
        decceleration = host.heading.multiply(host.beta)
        host.acceleration = host.acceleration - decceleration
