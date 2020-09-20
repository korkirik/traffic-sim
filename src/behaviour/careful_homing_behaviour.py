from behaviour.homing_behaviour import HomingBehaviour
from pvector import Pvector
from node import Node

class CarefulHomingBehaviour(HomingBehaviour):

    def __init__(self, host):
        super().__init__(host)
        host.agent_type = 'careful_homing'
        host.v_max = host.v_max * 0.75
        host.agent_range = 1.25 * host.agent_range
        host.detection_angle = host.detection_angle * 1.25
        host.patience_decrement = 0.5

    def update_behaviour(self):
        host = self.host

        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(host.agent_range, host.detection_angle)
        #self.detect_agents_in_sector(agent.agent_close_range, 90)
        self.detect_agents_rightward()
