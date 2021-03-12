from vehicle import *
from path import *


class NormalDriver:
    
    def __init__(self, posX, posY, _id, maxV, Path, Vehicle):
        
        self.posX = float(posX)
        self.posY = float(posY)
        self._id = int(_id)
        self.maxV = float(maxV)
        
        #setInitDest(p)
        syncTime = globalTime
    
    
    def move(Vehicle):
    
        crashedInFront = false
    
        applyBehaviour(vehicles)
    
        if(crashedInFront == true):
        
            Pvector.breakForce = Pvector.multiply(velocity, -1)
            acceleration.multiply(0)
            applyForce(breakForce)
    
            checkNumOfAccidentMet()
        
    
        ifCrashed()
    
        syncTime+=1
        localTime+=1
    
    
    def makeTurn(Path):
    
        #is true if the car is arrived at the "drive out" point and ready to make turn
        if(setGoal() & isArrived()):
        
            for i in range(0, len(path.mainJunctions[tempGoal].subJunctions)):
            
                #check only the "drive in" points in this junction and if they are accesssible
                if(isInOrOut(Path, this.tempGoal, i, 1) & isAccessible(Path, this.tempGoal, i)):
                
                    JunctionPoint.point = p.mainJunctions[tempGoal].subJunctions[i].get()
    
                    #randomly choose one junction points, and set it as goal
                    this.possibleDest.push_back(point)
            
            
    
            options = int(this.possibleDest.size())
            decision = int(rand() % options)
    
            this.goal = this.possibleDest[decision].get()
    
            this.possibleDest.clear()
    
            goals.erase (goals.begin())
            goals.push_back(goal)
    
            this.counter += 1
    
    def arrive(Vehicle):
    
        Pvector.sum = Pvector(0,0)
    
        #Find if anyone is in front of me
        findSomeoneInFront(vehicles)
    
        if(followSomeone == false & goal.inOrOut == 0):
        
            for i in range(0, len(possibleCars)):
            
                sameGoal = float(Pvector.distanceBetween(goal, possibleCars[i].goal))
                tempD = float(10000)
    
                if(sameGoal == 0 & possibleCars[i].goal.inOrOut == goal.inOrOut):
                
                    myDistToThere = float(Pvector.distanceBetween(goal, location))
                    hisDistToThere = float(Pvector.distanceBetween(possibleCars[i].goal, possibleCars[i].location))
    
                    distToHim = float(Pvector.distanceBetween(possibleCars[i].location, location))
    
                    if(hisDistToThere < myDistToThere & distToHim < tempD):
                    
                        followSomeone = true
                        whoIfollowed = i
                        tempD = distToHim
    
    
        if(followSomeone == true & goal.inOrOut == 0):
        
            #check the distance and the guy driving ahead
            distToSomeone = float(Pvector.distanceBetween(possibleCars[whoIfollowed].location, location))
    
            #Stay where i am at the moment i find him
            if(velocity.mag() != 0):
            
                mySteerForce = velocity.get()
                mySteerForce.mult(-1)
                summ = mySteerForce
    
            
            #Wait and do nothing until someone in front is already 30 pixel away
            #elif(distToSomeone < 20):
                
            
            #Cannot not find anyone to follow? okay, then go where you planned to go
            else:
            
                summ = goToJunction()
            
        
        else:
        
            summ = goToJunction()
        
    
        possibleCars.clear()
        return summ
    
    
    def goToJunction():
    
        Pvector.desired = Pvector.subtract(this.goal, this.location)
    
        d = float(desired.mag())
        desired.normalize()
    
        if(d < 100):
        
            m = float(map(d, 0, 100, 0, maxspeed))
            desired.mult(m)
        
        else:
        
            desired.mult(maxspeed)
        
    
        Pvector.steer = Pvector.subtract(desired, this.velocity)
        steer.limit(maxforce)
    
        followSomeone = false
        return steer
    
    
    def separate(Vehicle):
    
        desiredSeperation = float(10)
        tooClosecount = int(0)
        radius = int(50)
        Pvector.sum = Pvector(0,0)
        '''
        for i in range(std::vector<Vehicle*>::iterator it = vehicles.begin() ; it != vehicles.end(); ++it )
        
            float d = Pvector::dist(location, (*it)->location)
    
            /* Calculate vector pointing to neighbor */
            Pvector *pointToSomeone = Pvector::sub( (*it)->location, location)
            Pvector *myDirection = Pvector::sub(goal, location)
            float angle = Pvector::angleBetween(myDirection, pointToSomeone)
    
            if (d < radius && d > 0 && crashed == false)
            
                /* If distance to other vehicle is too close, then we assume they're crashed */
                if (d < 3)
                
                    crashed = true
                    numOfAcc = 1
                    memory = syncTime
                
                else if( d < 20 && angle < 20 && (*it)->crashed == true )
                
                    crashedInFront = true
                
    
                if (d < desiredSeperation)
                
                    Pvector *diff = Pvector::sub(location, (*it)->location)
                    diff->normalize()
                    diff->div(d)
    
                    sum->add(diff)
                    tooClosecount ++
    
        #Average
        '''
        if(tooClosecount > 0):
        
            if(tooClosecount > 3 & tooClosecount < 7):     #simulating a traffic jam
            
                summ.div(tooClosecount)
                summ.setMag(0)
            
            else: 
                summ.div(tooClosecount)
                summ.setMag(maxspeed)
            
        
    
        if (summ.mag() > 0):
        
            summ.setMag(maxspeed)
            summ.sub(velocity)
            summ.limit(maxforce)
        
    
        #returns the force vector to be applied
        return sum
    
    def follow():
    
        Pvector.here = Pvector(0,0)
        here = this.goals[myCurrentGoal].get()
    
        worldRecord = float(1000000)
    
        Pvector.there = Pvector(0,0)
        there = this.goals[myCurrentGoal + 1].get()
        Pvector.foll = Pvector(0,0)
    
        Pvector.predict = velocity.get()
        predict.normalize()
        predict.mult(25)
        Pvector.predictLoc = Pvector.add(location, predict)
    
        #Single path
    
        Pvector.normalPoint = Pvector.getNormalPoint(predictLoc, here, there)
    
        if(normalPoint.x < fmin(here.x, there.x) or normalPoint.x > fmax(here.x, there.x)):
        
            normalPoint = there.get()
        
        elif(normalPoint.y < fmin(here.y, there.y) or normalPoint.y > fmax(here.y, there.y)):
        
            normalPoint = there.get()
        
    
        Pvector.dir = Pvector.subtract(there, here)
        dir.normalize()
        dir.mult(10)
        Pvector.target = Pvector.add(normalPoint, dir)
    
        if (worldRecord > 5):
        
            foll = seek(target)
        
    
        #returns the force required to follow a path
        return foll
    
    def applyBehaviour(Vehicle):
    
        Pvector.sep = separate(vehicles)
        Pvector.arr = arrive(vehicles)
        Pvector.foll = follow()
    
        #weight for seperate behaviour (high value will mean high consideration for *seperation*)
        sep.mult(0.4)
        arr.mult(1)
        foll.mult(0.4)
    
        applyForce(sep)
        applyForce(arr)
        applyForce(foll)