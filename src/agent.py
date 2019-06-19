from pvector import *

class Agent:
    
    def __init__(self,x,y,maxVelocity, agent_id):
        
        self.x = float(x)
        self.y = float(y)
        self.vMax = float(maxVelocity)
        self.agentId = agent_id

        self.position = Pvector(x,y)
        self.velocity = Pvector(0,0)
        self.acceleration = Pvector(0,0)
        self.goal = node(0,0,0)
        
        agent = (x,y,vMax,agentID,position,velocity,acceleration,goal)
    
    def move(agent):
    
        movement = applyBehaviour(agent)
        
        acceleration = pvector.multiply(0)
        velocity = pvector.add(acceleration)
        velocity = pvector.limitMagnitude()
        position = pvector.add(velocity)
    
    def applyBehaviour():
        
        separate = pvector.distanceBetween()
    
        separate = pvector.multiply(1)
        
        separate = applyForce(separate)
        
        return separate
    
    def applyForce():
    
        force = Pvector.divide()
        acceleration = pvector.add(force)
    
'''
pswarm_main_run-5.py purpose and how it can be used for the agents
Which classes are required to inherit from?
Setting initial and final destination.  Is it required?
Interfacing with map?  Simulation?
'''
