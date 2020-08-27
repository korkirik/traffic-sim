from behaviour.behaviour import Behaviour
from pvector import Pvector
from node import Node

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
