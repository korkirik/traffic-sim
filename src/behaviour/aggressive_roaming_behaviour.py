from behaviour.roaming_behaviour import *
from pvector import Pvector
from node import Node

class AggressiveRoamingBehaviour(RoamingBehaviour):

    def __init__(self, host):
        self.host = host

        host.agent_type = 'aggressive_roaming'
        host.set_v_max(host.v_max * 1.25)
        host.agent_range = 0.75 * host.agent_range
        host.detection_angle = host.detection_angle * 0.5

    def update_behaviour(self):
        host = self.host

        host.patience_check()
        self.reset_acceleration()
        self.next_node_attraction()
        self.detect_agents_in_sector(host.agent_range, host.detection_angle)
