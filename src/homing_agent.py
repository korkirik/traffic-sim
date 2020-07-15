from pvector import *
from node import *
from agent import Agent

class HomingAgent(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.target_node = None
        self.target_vector = Pvector(0,0)
        self.agent_type = 'homing'
        self.preceding_node = None

    def set_starting_node(self, start_node):
        self.node_out = start_node
        self.position = start_node.position

    def set_target_node(self, node):
        self.target_node = node
        if(self.node_out == node):
            self.node_in = node
            print('start node is already at the target, setting inactive')
            self.set_inactive() # TODO: here should be inactivation, so calls of the functions are not affecting agent
        else:
            self.update_target()
            self.find_initial_heading()
            self.update_next_node_vector()

#-------------Main Logic-----------------

    def update_position(self): # TODO: replace
        self.position = self.position + self.velocity
        self.update_next_node_vector()

        if(self.distance_to_next_node < self.approach_error):

            self.update_target()
            if self.check_if_arrved():
                self.position = self.position - self.velocity #step back
                self.set_inactive()
            else:
                self.node_out = self.node_in
                self.pick_node()
                self.update_next_node_vector()
                self.velocity = Pvector.turn_vector(self.heading, self.velocity)

#-----------------------------------------
    def check_if_arrved(self):
        if(self.target_vector.magnitude() < self.approach_error):
            return True
        else:
            return False

    def update_target(self):
        self.target_vector = self.target_node.position - self.position
        self.target_distance = self.target_vector.magnitude()

    def find_initial_heading(self):
        i = self.find_node_towards_direction(self.target_vector)
        self.node_in = self.node_out.connected_nodes[i]

    def pick_node(self):
        #one node means turning around
        if(len(self.node_out.connected_nodes) == 1):
            index = 0
        #two nodes means a continuation of the street, agent moves along
        elif(len(self.node_out.connected_nodes) == 2):
            index = self.find_node_towards_direction(self.heading) # vector forward
        #agent decides at intersection which path is next
        else:
            index = self.find_node_towards_direction(self.target_vector)
        self.node_in = self.node_out.connected_nodes[index]

    def find_node_towards_direction(self, vector):
        angles = list()
        for index, node in enumerate(self.node_out.connected_nodes):
            direction = Pvector(0,0)
            direction = node.position - self.node_out.position
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
