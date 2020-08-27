from behaviour.homing_behaviour import HomingBehaviour
from pvector import Pvector
from node import Node

class AggressiveHomingBehaviour(HomingBehaviour):

    def __init__(self, agent):
        super().__init__(agent)
        agent.agent_type = 'aggressive_homing'


    #defined in roaming behaviour
    #def update_behaviour(self):
    #def update_velocity(self):

    def reached_next_node(self):
        pass
