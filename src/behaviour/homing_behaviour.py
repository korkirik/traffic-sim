from behaviour.behaviour import Behaviour
from behaviour.roaming_behaviour import RoamingBehaviour
from behaviour.reached_behaviour import ReachedBehaviour
from pvector import Pvector
from node import Node

import math

class HomingBehaviour(Behaviour):

    def __init__(self, agent):
        self.host = agent
        agent.agent_type = 'homing'

        agent.target_node = None
        agent.target_vector = Pvector(0,0)
        agent.preceding_node = None

    def set_starting_node(self, start_node):
        agent = self.host

        agent.node_out = start_node
        agent.position = start_node.position

    def find_initial_heading(self):
        agent = self.host

        i = self.find_node_towards_direction(agent.target_vector)
        agent.node_in = agent.node_out.connected_nodes[i]

    def set_target_node(self, node):
        agent = self.host

        agent.target_node = node
        if(agent.node_out == node):
            agent.node_in = node
            print('start node is already at the target, setting inactive')
            agent.set_inactive() # TODO: here should be inactivation, so calls of the functions are not affecting agent
        else:
            self.update_target()
            self.find_initial_heading()
            self.update_next_node_vector()

    def pick_next_node(self):
        agent = self.host

        #one node means turning around
        if(len(agent.node_out.connected_nodes) == 1):
            index = 0
        #two nodes means a continuation of the street, agent moves along
        elif(len(agent.node_out.connected_nodes) == 2):
            index = self.find_node_towards_direction(agent.heading) # vector forward
        #agent decides at intersection which path is next
        else:
            index = self.find_node_towards_direction(agent.target_vector)
        agent.node_in = agent.node_out.connected_nodes[index]

    def find_node_towards_direction(self, vector):
        agent = self.host
        angles = list()
        for index, node in enumerate(agent.node_out.connected_nodes):
            direction = Pvector(0,0)
            direction = node.position - agent.node_out.position
            #direction.show()
            #self.target_vector.show()
            angle = Pvector.angle_between(direction, vector)
            angles.append(angle)
        #print(angles)

        smallest_angle = 180
        index = 0
        for i, angle in enumerate(angles):
            if math.fabs(angle) < smallest_angle:
                smallest_angle = math.fabs(angle)
                index = i

        return index

    #defined in roaming behaviour
    #def update_behaviour(self):
    #def update_velocity(self):

    def reached_next_node(self):
        pass
#---------------------------------------
    def update_behaviour(self):
        agent = self.host

        agent.patience_check()
        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(agent.agent_range, agent.detection_angle)
        #self.detect_agents_in_sector(agent.agent_close_range, 90)
        self.detect_agents_rightward()

    def update_velocity(self):
        agent = self.host

        if (self.is_velocity_negative()):
            agent.velocity = Pvector(0,0)
        else:
            agent.velocity = agent.velocity + agent.acceleration
            agent.velocity.limit_magnitude(agent.v_max)

    def update_position(self):
        agent = self.host

        agent.position = agent.position + agent.velocity
        self.update_next_node_vector()

        if(agent.distance_to_next_node < agent.approach_error):

            self.update_target()
            if self.check_if_arrved():
                agent.position = agent.position - agent.velocity #step back
                agent.my_behaviour = ReachedBehaviour(agent)
            else:
                agent.node_out = agent.node_in
                self.pick_next_node()
                self.update_next_node_vector()
                agent.velocity = Pvector.turn_vector(agent.heading, agent.velocity)

#---------------------------------------
    def update_target(self):
        agent = self.host

        agent.target_vector = agent.target_node.position - agent.position
        agent.target_distance = agent.target_vector.magnitude()

    def check_if_arrved(self):
        agent = self.host

        if(agent.target_vector.magnitude() < agent.approach_error):
            return True
        else:
            return False
