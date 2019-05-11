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
from std import *

posX = 0
posX = float(posX)
posY = 0
posY = float(posY)
_id = 0
_id = int(_id)
maxV = 0
maxV = float(maxV)

def RoamingDriver(posX, posY, _id, maxV):

    Vehicle(posX, posY, _id, maxV)


def move():

    #It is assumed that std is another class which is being evoked here. Proper documentation is required to call the relevant functions.
    #std::vector<Vehicle *> vehicles

    applyBehaviour(vehicles);


def applyBehaviour():

    #See comment above for the same instance of this class evocation.
    #std::vector<Vehicle*> vehicles

    #The following variables are not clear and need to be defined correctly.
    '''
    //Pvector* sep = separate(vehicles);
    Pvector* arr = arrive(vehicles);
    Pvector* foll = follow();

    foll->mult(0.2);
    //sep->mult(1);
    arr->mult(1);

    //applyForce(sep);
    applyForce(foll);
    applyForce(arr);
    '''
