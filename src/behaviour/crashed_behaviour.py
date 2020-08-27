from pvector import Pvector
from node import Node
from behaviour.behaviour import Behaviour
from pvector import Pvector
from node import Node

class CrashedBehaviour(Behaviour):

    def __init__(self, agent):
        self.host = agent

        agent.active = 0
        #agent.velocity = Pvector(0,0)
        agent.agent_type = 'crashed'
        self.reset_acceleration()
        self.brake()
