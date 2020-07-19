from pvector import *
from node import *
from behaviour.behaviour import *
from behaviour.roaming_behaviour import *
import random

class CarefulRoamingBehaviour(RoamingBehaviour):

    def __init__(self, agent):
        self.my_agent = agent

        agent.agent_type = 'careful_roaming'
        agent.v_max = 0.75
        agent.agent_range = 1.25 * agent.agent_range
        agent.detection_angle = agent.detection_angle * 1.25
        self.patience_threshold = 30
        agent.patience_increment = 0.75
