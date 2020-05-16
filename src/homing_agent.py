from pvector import *
from node import *
from agent import Agent

class HomingAgent(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.target_node = None
        self.target_vector = Pvector(0,0)

    def set_starting_node(self, start_node):
        self.node_out = start_node
        self.position = start_node.position

    def set_target_node(self, node):
        self.target_node = node
        if(self.node_out == node):
            self.node_in = node
            print('start node is the target, setting inactive')
            self.set_inactive() # TODO: here should be inactivation, so calls of the functions are not affecting agent
        else:
            self.update_target()
            self.pick_node()

#-------------Main Logic-----------------
    ## TODO: Gather all behaviours here
    def update_behaviour(self):
        self.reset_acceleration()
        self.next_node_attraction()
        self.agents_aversion()

    def update_velocity(self):
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit_magnitude(self.v_max)


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

#-----------------------------------------
    def check_if_arrved(self):
        if(self.target_vector.magnitude() < self.approach_error):
            return True
        else:
            return False

    def update_target(self):
        self.target_vector = self.target_node.position - self.position
        self.target_distance = self.target_vector.magnitude()

    def pick_node(self):
        #if(len(self.node_out.connected_nodes) != 1):
        angles = list()
        for index, node in enumerate(self.node_out.connected_nodes):
            direction = Pvector(0,0)
            direction = node.position - self.node_out.position
            direction.show()
            self.target_vector.show()
            angle = Pvector.angle_between(direction,self.target_vector)
            angles.append(angle)

        print(angles)

        smallest_angle = 180
        index = 0
        for i, angle in enumerate(angles):
            if math.fabs(angle) < smallest_angle:
                smallest_angle = math.fabs(angle)
                index = i

        self.node_in = self.node_out.connected_nodes[index]
