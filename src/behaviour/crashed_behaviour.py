from pvector import *
from node import *
from behaviour.behaviour import *
import random

class CrashedBehaviour(Behaviour):

    def __init__(self, agent):
        self.my_agent = agent

        agent.active = 0
        #agent.velocity = Pvector(0,0)
        agent.agent_type = 'crashed'
        agent.reset_acceleration()
        agent.brake()
