from pvector import Pvector
from node import Node
from behaviour.behaviour import *

class ReachedBehaviour(Behaviour):

    def __init__(self, agent):
        self.host = agent

        agent.active = 0
        #agent.velocity = Pvector(0,0)
        agent.agent_type = 'reached_goal'
        agent.reset_acceleration()
        agent.brake()
