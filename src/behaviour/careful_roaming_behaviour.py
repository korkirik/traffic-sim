from behaviour.roaming_behaviour import *
from pvector import Pvector
from node import Node

class CarefulRoamingBehaviour(RoamingBehaviour):

    def __init__(self, agent):
        self.host = agent

        agent.agent_type = 'careful_roaming'
        agent.v_max = 0.75
        agent.agent_range = 1.25 * agent.agent_range
        agent.detection_angle = agent.detection_angle * 1.25
        self.patience_threshold = 30
        agent.patience_decrement = 0.5
