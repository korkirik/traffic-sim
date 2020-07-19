from pvector import *
from node import *
from converter import Converter
from behaviour.behaviour import *
from behaviour.roaming_behaviour import *
from behaviour.aggressive_roaming_behaviour import *
from behaviour.careful_roaming_behaviour import *
from behaviour.crashed_behaviour import *
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

        self.patience = 100 # percent
        self.patience_increment = 1
        self.patience_threshold = 50

        #if distance is < than that agent crashes
        self.critical_distance = 2 * self.alpha
        self.set_behaviour(type)

#--------------setters-------------------
    def set_behaviour(self, type):
        self.my_behaviour = Behaviour()
        if(type == 'roaming'):
            self.my_behaviour = RoamingBehaviour(self)
        elif(type == 'careful_roaming'):
            self.my_behaviour = CarefulRoamingBehaviour(self)
        elif(type == 'aggressive_roaming'):
            self.my_behaviour = AggressiveRoamingBehaviour(self)


    def set_starting_node(self, start_node):
        self.preceding_node = None
        self.node_out = start_node
        self.position = start_node.position
        self.my_behaviour.pick_next_node()

    def add_agent_list(self, agent_list):
        self.agent_list = agent_list

    def randomize_velocity(self):
        self.set_v_max(self.v_max + random.randrange(0,10,1)*0.01*self.v_max)

    def set_v_max(self, v_max):
        self.v_max = v_max
        self.reset_initial_parameters()

    def reset_initial_parameters(self):
        self.alpha = self.v_max/4
        self.beta =  2 * self.alpha
        self.approach_error = 2 * self.alpha
#------------State Flow/Control---------------

    # TODO: test
    def patience_check(self):
        if(self.velocity.magnitude() == 0): #for homing agent: and goal is not reached
            self.patience -= self.patience_increment
        #behaviour change
        if(self.patience < self.patience_threshold):
            self.my_behaviour = AggressiveRoamingBehaviour(self)
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
        self.active = 0
#-------------Main Logic-----------------
    ## TODO: Gather all behaviours here
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
            print(n.node_id) ## TODO: remove

    def next_node_attraction(self):
        self.acceleration = self.acceleration + self.heading.multiply(self.alpha)

#-------------Piloting------------------

    def update_next_node_vector(self):
        vector_next_node = Pvector(self.node_in.position.x, self.node_in.position.y)
        vector_next_node = vector_next_node - self.position
        self.distance_to_next_node = vector_next_node.magnitude()
        vector_next_node.normalize()
        self.heading = vector_next_node.copy()

    def reset_acceleration(self):
        self.acceleration = Pvector(0,0)
    # TODO: is there need for delta_vector?
    def brake(self, delta_vector = Pvector(0,0)):
        #constatnt brake force # TODO: gradient of brake force
        decceleration = self.heading.multiply(self.beta)
        self.acceleration = self.acceleration - decceleration

    def is_velocity_negative(self):

        v1 = self.velocity + self.acceleration
        if(Pvector.dot_product(v1, self.heading) <= 0):
            return True
        else:
            return False
