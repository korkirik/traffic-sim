from behaviour.homing_behaviour import HomingBehaviour
from behaviour.reached_behaviour import ReachedBehaviour
from pvector import Pvector
from node import Node

import math

class BusBehaviour(HomingBehaviour):

    def __init__(self, host):
        self.host = host
        host.agent_type = 'bus'

        self.boarding_time = 300 ## TODO: tune this parameter
        self.waiting_iteration = 300
        self.current_target = None
        self.target_list = list()
        self.target_vector = Pvector(0,0)
        host.preceding_node = None

    def check_if_at_bus_stop(self):
        if self.current_target.type == 'bus_stop':
            return True
        else:
            return False

    def check_if_still_boarding(self):
        if self.waiting_iteration < self.boarding_time:
            self.waiting_iteration =  self.waiting_iteration + 1
            return True
        else:
            return False

    def update_velocity(self):
        host = self.host

        if (self.is_velocity_negative()):
            host.velocity = Pvector(0,0)
        else:
            host.velocity = host.velocity + host.acceleration
            host.velocity.limit_magnitude(host.v_max)

        if(self.check_if_still_boarding()):
            host.velocity = Pvector(0,0)


    def update_position(self):
        host = self.host

        host.position = host.position + host.velocity
        self.update_next_node_vector()

        self.update_target()
        if self.check_if_arrved():
            host.position = host.position - host.velocity #step back
            #print('I am at {}'.format(self.current_target.name))
            if self.check_if_at_bus_stop():
                self.waiting_iteration = 0 #set boarding counter
                print('I am at {}'.format(self.current_target.name))
            self.select_next_target()

        if(host.distance_to_next_node < host.approach_error):
            host.preceding_node = host.node_out
            host.node_out = host.node_in
            self.pick_next_node()
            self.update_next_node_vector()
            host.velocity = Pvector.turn_vector(host.heading, host.velocity)

    def boarding_curbside(self):
        pass #wait for x iterations

    def boarding_busbay(self):
        pass
