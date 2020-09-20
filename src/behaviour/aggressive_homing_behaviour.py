from behaviour.homing_behaviour import HomingBehaviour
from pvector import Pvector
from node import Node

class AggressiveHomingBehaviour(HomingBehaviour):

    def __init__(self, host):
        super().__init__(host)
        host.agent_type = 'aggressive_homing'
        host.v_max = host.v_max * 1.25
        host.agent_range = 0.75 * host.agent_range
        host.detection_angle = host.detection_angle * 0.5

    def update_behaviour(self):
        host = self.host

        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(host.agent_range, host.detection_angle)
        #self.detect_agents_in_sector(agent.agent_close_range, 90)
        #self.detect_agents_rightward()
