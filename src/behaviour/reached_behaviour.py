from behaviour.behaviour import Behaviour
from pvector import Pvector
from node import Node

class ReachedBehaviour(Behaviour):

    def __init__(self, agent):
        self.host = agent

        agent.active = 0
        #agent.velocity = Pvector(0,0)
        agent.agent_type = 'reached_goal'
        self.reset_acceleration()
        self.brake()
