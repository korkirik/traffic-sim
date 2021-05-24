#include "drunkdriver.h"

import path as p
from vehicle import *
from pvector import Pvector

class DrunkDriver:

    def _init_(self, posX, posY, _id, maxV, p, globalTime):
        
        self.setInitDest = p, _id
        
        self.syncTime = globalTime   
    
    def move(Vehicle):
    
        crashedInFront = false
    
        applyBehaviour(vehicles)
        
        velocity = float(0)
        acceleration = float(0)
    
        if(crashedInFront == true):
        
            breakForce = Pvector.multiply(velocity, -1)
            acceleration = Pvector.multiply(acceleration,0)
            applyForce(breakForce)
    
            checkNumOfAccidentMet()
          
        ifCrashed()
        
        location = float(0)
        longTermDest = float(0)
    
        tmpDist = float(Pvector.distanceBetween(location, longTermDest))
        
        reachedDest = bool
        
        localtime = float(0)
        
        if( tmpDist < 20 ):
        
            reachedDest = true
            lot = localTime
        
    
        if(reachedDest != true):
        
            syncTime +1
            localTime +1
    
    def makeTurn(p):    
        
        tempGoal = float(0)
        
        #Is true if the car is arrived at the "drive out" point and ready to make turn
        if(setGoal() & isArrived()):
        
            for i in range (0, len(p.mainJunctions(tempGoal).subJunctions)):
            
                #check only the "drive in" points in this junction and if they are accesssible
                if(isInOrOut(p, this.tempGoal, i, 1) & isAccessible(p, this.tempGoal, i)):
    
                    JunctionPointPoint = p.mainJunctions(tempGoal).subJunctions(i).get()
    
                    #randomly choose one junction points, and set it as goal
                    this.possibleDest.append(JunctionPointPoint)             
            
            options = this.possibleDest.size()
    
            destVec = Pvector.subtract(longTermDest, tempGoal)
    
            tempChoice = int(0)
            tempAngle = float(1800)
    
            for i in range(0, len(options)):
            
                tmpVec = Pvector.subtract(possibleDest[i], tempGoal)
                angle = float(Pvector.angleBetween(destVec, tmpVec))
    
                if(angle < tempAngle):
                
                    tempAngle = angle
                    tempChoice = i          
            
            this.goal = this.possibleDest(tempChoice).get()
    
            this.possibleDest.clear()
    
            goals.erase (goals.begin())
            goals.append(goal)
    
            this.counter + 1
            
    
    def follow(Pvector):
    
        Pvector.here = newPvector(0,0)
        here = this.goals[myCurrentGoal].get()
    
        Pvector.there = newPvector(0,0)
        there = this.goals[myCurrentGoal + 1].get()
    
        worldRecord = float(1000000)
        Pvector.foll =  newPvector(0,0)
    
        Pvector.predict = velocity.get()
        predict.normalize()
        predict.multiply(25)
        Pvector.predictLoc = Pvector.add(location & predict)
    
        Pvector.normalPoint = Pvector.getNormalPoint(predictLoc, here, there)
    
        if(normalPoint.x < fmin(here.x, there.x) or normalPoint.x > fmax(here.x, there.x)):
        
            normalPoint = there.get()
        
        elif(normalPoint.y < fmin(here.y, there.y) or normalPoint.y > fmax(here.y, there.y)):
        
            normalPoint = there.get()
        
    
        Pvector.direction = Pvector.subtract(there, here)
        direction.normalize()
        direction.mult(10)
        Pvector.target = Pvector.add(normalPoint, direction)
    
        #5 is the path radius
        if (worldRecord > 5):
        
            foll = seek(target)
    
        return foll
    
    def separate(Pvector, Vehicle):
    
        #5 = radius of car object
        desiredSeperation = float(10 * 2)
        tooClosecount = int(0)
        radius = int(50)
        Pvector.sum = newPvector(0,0)
    
        '''
        for i in range (Pvector.iterator = vehicles.begin(), vehicles.end()):
        
            d = float(Pvector.dist(location, (i).location))
    
            #Calculate vector pointing to neighbor
            Pvector.pointToSomeone = Pvector.subtract((i).location, location)
            Pvector.myDirection = Pvector.subtract(goal, location)
            angle = float(Pvector.angleBetween(myDirection, pointToSomeone))
    
            if (d < radius & d > 0 & crashed == false):
            
                #If distance to other vehicle is too close, then it must have been crashed.
                if (d < 3 & localTime > 200):
                
                    crashed = true
                    numOfAcc = 1
                    memory = syncTime
                    lot = 0
                
                elif(d < 20 & angle < 20 & (i).crashed == true):
                
                    crashedInFront = true
                
    
                if (d < desiredSeperation):
                
                    Pvector.diff = Pvector.subtract(location, (i).location)
                    diff.normalize()
                    diff.div(d)
    
                    summ.add(diff)
                    tooClosecount + 1
       '''         
            
    
        #Average
    
        if(tooClosecount > 0):
        
            #simulating a traffic jam
            if(tooClosecount > 3 & tooClosecount < 7):
            
                summ.divide(tooClosecount)
                summ.setMagnitude(0)
            
            else: 
                summ.divide(tooClosecount)
                summ.setMagnitude(maxspeed)
            
        
    
        if (summ.mag() > 0):
        
            summ.setMagnitude(maxspeed)
            summ.subtract(velocity)
            summ.limit(maxforce)
        
        return summ
    
    
    
    def arrive(Pvector, Vehicle):
    
        Pvector.summ = newPvector(0,0)
    
        #Find if anyone is in front of me
        findSomeoneInFront(vehicles)
    
        if(followSomeone == false & goal.inOrOut == 0):
        
            for i in range (0, len(possibleCars)):
            
                sameGoal = float(Pvector.dist(goal, possibleCars[i].goal))
                tempD = float(10000)
    
                if(sameGoal == 0 & possibleCars[i].goal.inOrOut == goal.inOrOut):
                
                    myDistToThere = float(Pvector.dist(goal, location))
                    hisDistToThere = float(Pvector.dist(possibleCars[i].goal, possibleCars[i].location))
                    distToHim = float(Pvector.dist(possibleCars[i].location, location))
    
                    if(hisDistToThere < myDistToThere & distToHim < tempD):
                    
                        followSomeone = true
                        whoIfollowed = i
                        tempD = distToHim
                    
    
    
        if(followSomeone == true & goal.inOrOut == 0):
        
            #check the distance and the guy driving ahead
            distToSomeone = float(Pvector.dist(possibleCars[whoIfollowed].location, location))
    
            #Stay where i am at the moment i find him
            if(velocity.magnitude() != 0):
            
                mySteerForce = velocity.get()
                mySteerForce.multiply(-1)
                summ = mySteerForce
    
            
            #Wait and do nothing until someone in front is already 30 pixel away
            elif(distToSomeone < 30):
                
                summ = summ
            
            #Cannot not find anyone to follow? okay, then go where you planned to go
            else:
                
                summ = goToJunction()
            
        else:
        
            summ = goToJunction()
        
    
        possibleCars.clear()
        return summ
    
    def applyBehaviour(Pvector, Vehicle):
    
        Pvector.sep = separate(vehicle)
        Pvector.arr = arrive(vehicle)
        Pvector.foll = follow()
    
        sepWeight = 1 * patience
        arrWeight = 1
        folWeight = 1 / patience
    
        #weight for seperate behaviour (high value will mean high consideration for *seperation*)
        sep.mult(sepWeight)
        arr.mult(arrWeight)
        foll.mult(folWeight)
    
        applyForce(sep)
        applyForce(arr)
        applyForce(foll)