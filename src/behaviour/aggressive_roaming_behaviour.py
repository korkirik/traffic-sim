from pvector import Pvector
from node import Node
from behaviour.behaviour import *
from behaviour.roaming_behaviour import *
import random

class AggressiveRoamingBehaviour(RoamingBehaviour):

    def __init__(self, agent):
        self.host = agent

        agent.agent_type = 'aggressive_roaming'
        agent.v_max = 1.25
        agent.agent_range = 0.75 * agent.agent_range
        agent.detection_angle = agent.detection_angle * 0.5

    def update_behaviour(self):
        agent = self.host

        agent.patience_check()
        agent.reset_acceleration()
        agent.next_node_attraction()
        self.detect_agents_in_sector(agent.agent_range, agent.detection_angle)
