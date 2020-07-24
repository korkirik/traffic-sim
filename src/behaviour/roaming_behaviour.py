from pvector import Pvector
from node import Node
from behaviour.behaviour import *
import random, math

class RoamingBehaviour(Behaviour):

    def __init__(self, agent):
        self.host = agent
        self.host.agent_type = 'roaming'

    def set_starting_node(self, start_node):
        agent = self.host
        agent.preceding_node = None
        agent.node_out = start_node
        agent.position = start_node.position
        self.pick_next_node()

    def pick_next_node(self):
        agent = self.host

        if(len(agent.node_out.connected_nodes) != 1):
            picked_number = self.random_roll()
            while(agent.node_out.connected_nodes[picked_number] == agent.preceding_node):
                picked_number = self.random_roll()
        else:
            picked_number = 0

        agent.node_in = agent.node_out.connected_nodes[picked_number]

    def random_roll(self):
        number = random.randint(0,len(self.host.node_out.connected_nodes)-1)  #pick random Node from available
        return number

    def reached_next_node(self):
        agent = self.host

        agent.preceding_node = agent.node_out
        agent.node_out = agent.node_in
        self.pick_next_node()
        agent.update_next_node_vector()
        agent.velocity = Pvector.turn_vector(agent.heading, agent.velocity)
#---------------------------------------

    def update_behaviour(self):
        agent = self.host

        agent.patience_check()
        agent.reset_acceleration()
        agent.next_node_attraction()
        self.detect_agents_in_sector(agent.agent_range, agent.detection_angle)
        #self.detect_agents_in_sector(agent.agent_close_range, 90)
        self.detect_agents_rightward()

    def update_velocity(self):
        agent = self.host

        if (agent.is_velocity_negative()):
            agent.velocity = Pvector(0,0)
        else:
            agent.velocity = agent.velocity + agent.acceleration
            agent.velocity.limit_magnitude(agent.v_max)

    def update_position(self):
        agent = self.host

        agent.position = agent.position + agent.velocity
        agent.check_crash()
        agent.update_next_node_vector()

        if(agent.distance_to_next_node < agent.approach_error):
            agent.my_behaviour.reached_next_node()
#---------------------------------------

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
                    host.brake(delta_vector)

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
                    host.brake(delta_vector)
