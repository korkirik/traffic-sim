from pvector import Pvector
from node import Node
from converter import Converter

from behaviour.behaviour import Behaviour
from behaviour.roaming_behaviour import RoamingBehaviour
from behaviour.aggressive_roaming_behaviour import AggressiveRoamingBehaviour
from behaviour.careful_roaming_behaviour import CarefulRoamingBehaviour
from behaviour.crashed_behaviour import CrashedBehaviour
from behaviour.homing_behaviour import HomingBehaviour
from behaviour.aggressive_homing_behaviour import AggressiveHomingBehaviour
from behaviour.careful_homing_behaviour import CarefulHomingBehaviour
from behaviour.inactive_behaviour import InactiveBehaviour
from behaviour.walker import Walker

import random, math

class Agent:

    def __init__(self, agent_id, type):

        self.position = Pvector(0,0)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.agent_id = agent_id

        self.v_max = 1 #0.1
        self.alpha = self.v_max/4
        self.beta =  2 * self.alpha # 1.15
        self.decceleration_magnitude = 0

        #self.minimal_separation = 0.00075 #75 *self.alpha
        self.approach_error = 2 * self.alpha
        self.agent_range = 40 *self.v_max
        self.agent_close_range = 10 * self.v_max
        self.detection_angle = 10

        self.agents_in_range = 0
        self.heading = Pvector(0,0)
        self.distance_to_next_node = 0
        self.active = 1

        self.delta = Pvector(0,0)

        self.patience = 100
        self.patience_decrement = 1
        self.patience_threshold = 50

        #if distance is < than that agent crashes
        self.critical_distance = 2 * self.alpha
        self.set_behaviour(type)

#--------------setters-------------------
    def set_behaviour(self, type):
        self.my_behaviour = Behaviour()
        self.not_aggressive = 1
        if(type == 'roaming'):
            self.my_behaviour = RoamingBehaviour(self)
        elif(type == 'careful_roaming'):
            self.my_behaviour = CarefulRoamingBehaviour(self)
        elif(type == 'aggressive_roaming'):
            self.my_behaviour = AggressiveRoamingBehaviour(self)
            self.not_aggressive = 0
        elif(type == 'homing'):
            self.my_behaviour = HomingBehaviour(self)
        elif(type == 'aggressive_homing'):
            self.my_behaviour = AggressiveHomingBehaviour(self)
            self.not_aggressive = 0
        elif(type == 'careful_homing'):
            self.my_behaviour = CarefulHomingBehaviour(self)
        elif(type == 'walker'):
            self.my_behaviour = Walker(self)
        else:
            self.my_behaviour = InactiveBehaviour(self)

    def set_starting_node(self, start_node):
        self.my_behaviour.set_starting_node(start_node)

    def set_closest_node(self, node):
        self.my_behaviour.set_closest_node(node)

    def set_target_node(self, target_node):
        # TODO: check if it is homing type
        self.my_behaviour.set_target_node(target_node)

    def add_agent_list(self, agent_list):
        self.agent_list = agent_list

    def randomize_velocity(self):
        self.set_v_max(self.v_max + random.randrange(0,10,1)*0.01*self.v_max)

    #sets max velocity, adjusts agent dynamics accordingly
    def set_v_max(self, v_max):
        self.v_max = v_max
        self.reset_initial_parameters()

    def reset_initial_parameters(self):
        self.alpha = self.v_max/4
        self.beta =  2 * self.alpha
        self.approach_error = 2 * self.alpha
        self.agent_range = 40 * self.v_max
        self.agent_close_range = 10 * self.v_max
#------------State Flow/Control---------------

    # TODO: test
    def patience_check(self):
        if(self.velocity.magnitude() == 0): #for homing agent: and goal is not reached
            self.patience -= self.patience_decrement

        #behaviour change
        if(self.not_aggressive):
            if(self.patience < self.patience_threshold):
                if isinstance(self.my_behaviour, RoamingBehaviour) or isinstance(self.my_behaviour, CarefulRoamingBehaviour):
                    self.my_behaviour = AggressiveRoamingBehaviour(self)
                    self.not_aggressive = 0
        #        if isinstance(self.my_behaviour, HomingBehaviour) or isinstance(self.my_behaviour, CarefulHomingBehaviour):
                    #behaviour
        #            self.my_behaviour = AggressiveHomingBehaviour(self)
                #c = Converter()
                #long, lat = c.convert_point_to_geocoordinates(self.position.x, self.position.y)
                #print('agent# {} ran out of patience at {},{}'.format(self.agent_id, long, lat))

    def check_crash(self):
        for agent in self.agent_list:
            if(agent != self):
                if(agent.active == 0):
                    continue

                if(Pvector.dot_product(agent.heading, self.heading) < 0):
                    continue

                distance = Pvector.distance_between_points(agent.position, self.position)
                if(distance < self.critical_distance):
                    self.crash()
                    agent.crash()
                    break
    # TODO: test
    def crash(self):
        self.my_behaviour = CrashedBehaviour(self)

    def set_inactive(self):
        self.my_behaviour = InactiveBehaviour(self)
#-------------Main Logic-----------------
    def update(self):
        self.my_behaviour.update_behaviour()
        self.my_behaviour.update_velocity()
        self.my_behaviour.update_position()
#-----------------------------------------
    def print_reachable_nodes(self):
        print('start connections:')
        for obj in self.node_out.connected_nodes:
            print(obj.node_id)

        print('next connections:')
        for n in self.node_in.connected_nodes:
            print(n.node_id)
