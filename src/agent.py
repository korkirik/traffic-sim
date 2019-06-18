from pvector import *

class Agent:
    def __init__(self,x,y,maxVelocity, agent_id):
        self.x = float(x)
        self.y = float(y)
        self.vMax = float(maxVelocity)
        self.agentId = agent_id

        self.location = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.steerForce = Pvector(0,0)
        self.longTermDest = Pvector(0,0)
        self.goal = JunctionPoint(0,0,0)
