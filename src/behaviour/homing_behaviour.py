from behaviour.behaviour import Behaviour
from behaviour.reached_behaviour import ReachedBehaviour
from pvector import Pvector
from node import Node

import math

class HomingBehaviour(Behaviour):

    def __init__(self, host):
        self.host = host
        host.agent_type = 'homing'

        host.target_node = None
        host.target_vector = Pvector(0,0)
        host.preceding_node = None

    def set_starting_node(self, start_node):
        host = self.host
        host.preceding_node = None
        host.node_out = start_node
        host.position = start_node.position

    def set_target_node(self, node):
        host = self.host

        host.target_node = node
        if(host.node_out == node):
            host.node_in = node
            print('start is in the target node, setting inactive')
            host.set_inactive() # TODO: here should be inactivation, so calls of the functions are not affecting agent
        else:
            self.update_target()
            self.find_initial_heading()
            self.update_next_node_vector()

    def find_initial_heading(self):
        host = self.host

        i = self.find_node_towards_direction(host.target_vector)
        host.node_in = host.node_out.connected_nodes[i]

    def pick_next_node(self):
        host = self.host

        #one node means turning around
        if(len(host.node_out.connected_nodes) == 1):
            index = 0
        #two nodes means a continuation of the street, agent moves along
        elif(len(host.node_out.connected_nodes) == 2):
            if(host.node_out.connected_nodes[0] == host.preceding_node):
                index = 1
            else:
                index = 0

        #agent decides at intersection which path is next
        else:
            index = self.find_node_towards_direction(host.target_vector)
        host.node_in = host.node_out.connected_nodes[index]

    def find_node_towards_direction(self, vector):
        host = self.host
        angles = list()
        for index, node in enumerate(host.node_out.connected_nodes):
            direction = Pvector(0,0)
            direction = node.position - host.node_out.position
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

    def reached_next_node(self):
        pass
#---------------------------------------
    def update_behaviour(self):
        host = self.host

        host.patience_check()
        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(host.agent_range, host.detection_angle)
        #self.detect_agents_in_sector(agent.agent_close_range, 90)
        self.detect_agents_rightward()

    def update_velocity(self):
        host = self.host

        if (self.is_velocity_negative()):
            host.velocity = Pvector(0,0)
        else:
            host.velocity = host.velocity + host.acceleration
            host.velocity.limit_magnitude(host.v_max)

    def update_position(self):
        host = self.host

        host.position = host.position + host.velocity
        self.update_next_node_vector()

        if(host.distance_to_next_node < host.approach_error):

            self.update_target()
            if self.check_if_arrved():
                host.position = host.position - host.velocity #step back
                host.my_behaviour = ReachedBehaviour(host)
            else:
                host.preceding_node = host.node_out
                host.node_out = host.node_in
                self.pick_next_node()
                self.update_next_node_vector()
                host.velocity = Pvector.turn_vector(host.heading, host.velocity)

                #print('Going to Node {}'.format(host.node_in.node_id))
#---------------------------------------
    def update_target(self):
        host = self.host

        host.target_vector = host.target_node.position - host.position
        host.target_distance = host.target_vector.magnitude()

    def check_if_arrved(self):
        host = self.host

        if(host.target_distance < host.approach_error):
            return True
        else:
            return False