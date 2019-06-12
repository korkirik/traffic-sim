'''
* Classname
*  - RoamingDriver
*
* Brief
*  - Implementation of roaming behavior
*
* Inherit
*  - class Vehicle
*
* Virtual Function
*  - void move()
*    void applyBehaviour()
*
* Detail
*  - Implement its own behavior (Roaming) by inheriting the
*    decision-related functions from Vehicle class.
'''

from vehicle import *

class RoamingDriver:
    
    def __init__(self, posX, posY, _id, maxV):
    
        self.posX = float(posX)
        self.posY = float(posY)
        self._id = int(_id)
        self.maxV = float(maxV)
        
        Vehicle(posX, posY, _id, maxV)
        
    
    def move(vehicle):
    
        applyBehaviour(vehicle)
    
    
    def applyBehaviour():
        
        Pvector.sep = separate(vehicles)
        Pvector.arr = arrive(vehicles)
        Pvector.foll = follow()
    
        foll.mult(0.2)
        sep.mult(1)
        arr.mult(1)
    
        applyForce(sep)
        applyForce(foll)
        applyForce(arr)