from pvector import *
from junctionpoint import *
from path import *

class Vehicle:

    def __init__(self, x, y, _id, v):
        
        self.x = float(x) 
        self.y = float(y) 
        self._id = int(_id) 
        self.v = float(v)
        
        location = Pvector(x,y)
        velocity = Pvector(0,0)
        acceleration = Pvector(0,0)
        mySteerForce = Pvector(0,0)
        longTermDest = Pvector(0,0)
        goal = JunctionPoint(0,0,0)        # A point that attracts agent
    
        counter = 0                        # To make sure only one behavior is being carried out at a time
        maxforce= 0.5 * v                  # Stronger the max force, more directly it's attracted 
        maxspeed= v                        # Higher the max speed, faster it goes 
        myCurrentGoal = 0                  # Work as an index pointing to the current goal in a vector
        onlyOnce = 0                       # A variable that make sure an if-statement runs only once
        whoIfollowed = 0                   # The index of the guy i am followed in terms of in an array(vector)
        id1 = _id                           # Identity */
        syncTime = 0
        localTime = 0
        lot = 0
        memory = 0
        NumAccidentMet = 0
        numOfAcc = 0
        carsAroundMe = 0
        patience = 1
    
        # Behaviour weight
        sepWeight = 0.4
        arrWeight = 1
        folWeight = 0.4
    
        # Give random value between 0.4 ~ 0.7
        patient_time = (rand() % 4 + 4) / 10.0
        patient_acci = (rand() % 4 + 4) / 10.0
        patient_cars = (rand() % 4 + 4) / 10.0
    
        # Boolean status 
        reachedDest == false
        followSomeone == false
        crashed == false
        crashedInFront == false
    
        goals.push_back(location)
    
        #///////// No Used Variable ////////
        mass = 1                           # No use
        
    #///////////////// Behaviors ///////////////   
                                                
    # Choose which main junction to go
    def chooseJunction(Path):
    
        distance = float(0)
        smallest = float(100000)
    
        # is true if the car is ready to drive in to a street (i.e. at an "in" point) 
        if(setGoal() & aboutToGo()):
        
            tempVar = tempGoal
    
            # get the index of the standing point in terms of all 8 junction points 
            #unsigned long index = this->goal->index;
    
            #calculate the corresponding position at the other junction to "drive out" 
            index = (index + 5) % 8
    
            for i in range(0, len(mainJunctions)):
            
                #if the point asked is accessible and it's not at my own junction
                if(isAccessible(p, i, index) & i != tempVar):
                
                    distance = Pvector.dist(p.mainJunctions[i].subJunctions[index], this.location)
    
                    if(distance < smallest):
                    
                        smallest = distance
    
                        #find out which junction has the cloest "drive out" point
                        tempGoal = i                 
    
            #set my goal to that junciton, in particular the corresponding point
            (this.goal) = p.mainJunctions[tempGoal].subJunctions[index].get()
    
            goals.erase (goals.begin())
            goals.push_back(goal)
    
            this.counter +=1
         
        #is true if the car is on a street or somewhere else, but not at the in/out points
        elif(setGoal() & onlyOnce == 0):
        
            for i in range(0, len(p.mainJunctions)):
            
                distance = Pvector.dist( p.mainJunctions[i].junLocation, this.location) # calculate the dist to all junctions
    
                if(distance <= smallest):
                
                    smallest = distance
                    tempGoal = i                                                            # find out which junction is the closet
                         
            # randomly pick up one junction point to arrive at the chosen junction
            for i in range(0, len(p.mainJunctions[tempGoal].subJunctions)):
            
                if(isInOrOut(p, this.tempGoal, i, 0) & isAccessible(p, this.tempGoal, i) != false):
    
                    JunctionPoint.point = p.mainJunctions[tempGoal].subJunctions[i].get()
    
                    this.possibleDest.push_back(point)
            
            options = int(this.possibleDest.size())
            decision = int(rand() % options)
    
            (this.goal) = this.possibleDest[decision].get()
            this.possibleDest.clear()
    
            goals.push_back(goal)
    
            this.counter +=1
            onlyOnce +=1
    
    # Choose which junction points to turn
    def makeTurn(Path):
    
        # is true if the car is arrived at the "drive out" point and ready to make turn 
        if(setGoal() & isArrived()):
    
            for i in range(0, len(p.mainJunctions[tempGoal].subJunctions)):
    
                # check only the "drive in" points in this junction and if they are accesssible 
                if(isInOrOut(p, this.tempGoal, i, 1) & isAccessible(p, this.tempGoal, i)):
                
                    JunctionPoint.point = p.mainJunctions[tempGoal].subJunctions[i].get()
    
                    # randomly choose one junction points, and set it as goal
                    this.possibleDest.push_back(point)
                    
            options = int(this.possibleDest.size())
            decision = int(rand() % options)
    
            (this.goal) = this.possibleDest[decision].get()
            this.possibleDest.clear()
    
            goals.erase (goals.begin())
            goals.push_back(goal)
    
            this.counter += 1
    
    # Driving towards my goal (junction points), but follow someone when he is there (No too close to him though)
    def arrive(Pvector):
    
        Pvector = Pvector(0,0)
    
        if(followSomeone == false & goal.inOrOut == 0):
    
            findSomeoneInFront(vehicles)
    
            for i in range(0, len(possibleCars)):
    
                sameGoal = float(Pvector.dist(goal, possibleCars[i].goal))
                tempD = float(10000)
    
                if(sameGoal == 0 & possibleCars[i].goal.inOrOut == goal.inOrOut):
    
                    myDistToThere = float(Pvector.dist(goal, location))
                    hisDistToThere = float(Pvector.dist(possibleCars[i].goal, possibleCars[i].location))
                    myReachingTime = float(myDistToThere / velocity.mag())
                    hisReachingTime = float(hisDistToThere / possibleCars[i].velocity.mag())
                    distToHim = float(Pvector.dist(possibleCars[i].location, location))
    
                    if(hisDistToThere < myDistToThere & distToHim < tempD):
                    
                        followSomeone = true
                        whoIfollowed = i
                        tempD = distToHim
                    
        if(followSomeone == true & goal.inOrOut == 0):
        
            # check the distance and the guy driving ahead 
            distToSomeone = float(Pvector.dist(possibleCars[whoIfollowed].location, location))
    
            # Stay where i am at the moment i find him
            if(velocity.mag() != 0):
            
                mySteerForce = velocity.get()
                mySteerForce.multiply(-1)
                summ = mySteerForce
    
            # Wait and do nothing until someone in front is already 30 pixel away 
            elif(distToSomeone < 20):
            
                summ = summ
            # Cannot not find anyone to follow? okay, then go where you planned to go
            else:
            
                summ = goToJunction()
            
        else:
        
            summ = goToJunction()
    
        possibleCars.clear()
        return summ
    
    def follow(Pvector):
    
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
        
        Pvector.dir = Pvector.sub(there, here)
        dir.normalize()
        dir.mult(10)
        Pvector.target = Pvector.add(normalPoint, dir)
    
        if (worldRecord > 5):
        
            foll = seek(target)
    
        return foll
    
    def separate():    # is not a void function now
    
        desiredSeperation = float(10 * 2) #5= radius of car object
        tooClosecount = int(0)
        radius = int(50)
        Pvector.sum = Pvector(0,0)
        '''
        for (std.vector(Vehicle).iterator it = vehicles.begin() ; it != vehicles.end(); ++it):
        
            d = float(Pvector.dist(location, it.location))
    
            if (d < radius):
            
                if ((d > 0) & (d < desiredSeperation)):
                
                    Pvector.diff = Pvector.sub(location, it.location)  #Calculate vector pointing away from neighbor
                    diff.normalize()
                    diff.div(d)
    
                    diff.mult(0)
                    #weight by distance
                    summ.add(diff)
                    tooClosecount +=1       #keeping track
                
        '''    
        #// Average //
    
        if(tooClosecount > 0):
        
            #simulating a traffic jam 
            if(tooClosecount > 3 & tooClosecount < 7):
            
                summ.div(tooClosecount)
                summ.setMag(0)
            
            else: 
                summ.div(tooClosecount)
                summ.setMag(maxspeed)
        
        
        if (summ.mag() > 0):
        
            summ.setMag(maxspeed)
            summ.sub(velocity)
            summ.limit(maxforce)
        
        # returns the force vector to be applied
        return summ
    
    # Behaviour function (following and separation)   (overwritten for drunk drivers in drunkdriver class) 
    def applyBehaviour():
    
        Pvector.sep = separate(vehicles)
        Pvector.foll = follow()
    
        sep.mult(1)       #weight for seperate behaviour (high value will mean high consideration for *seperation*)
        foll.mult(1)    #weight for follow behaviour (  "  *follow*)
        arr.mult(1.5)
    
        applyForce(sep)
        applyForce(foll)
        
    # Go to my goal (junction points)
    def goToJunction():
    
        Pvector.desired = Pvector.sub(this.goal, this.location)
    
        d = float(desired.mag())
        desired.normalize()
    
        if(d < 100):
        
            m = float(mapp(d, 0, 100, 0, maxspeed))
            desired.mult(m)
        
        else:
        
            desired.mult(maxspeed)
        
    
        Pvector.steer = Pvector.sub(desired, this.velocity)
        steer.limit(maxforce)
    
        followSomeone = false
        
        return steer
    
    def seek(Pvector):
    
        Pvector.desired = Pvector.sub(target, this.location)
        desired.normalize()
        desiredMax = float(maxspeed * 0.7)
        desired.mult(desiredMax)
    
        Pvector.steer= Pvector.sub(desired, this.velocity)
        steer.limit(maxforce)
        applyForce(steer)
    
        followSomeone = false
        
        return steer
    
    
    # Loop through all cars except myself, see if i can find someone driving ahead of me. If yes, then i will remember him. 
    def findSomeoneInFront():
    
        # Look around
        desiredSeperation = float(18)
    
        for i in range(0, len(vehicles)):
        
            # Calculate vector pointing to neighbor 
            Pvector.pointToSomeone = Pvector.sub(vehicles[i].location, location)
            Pvector.myDirection = Pvector.sub(goal, location)
            angle = float(Pvector.angleBetween(myDirection, pointToSomeone))
    
            d = float(pointToSomeone.mag())
    
            if(d != 0 & d <= desiredSeperation & angle < 20):
            
                possibleCars.push_back(vehicles[i])
            
        carsAroundMe = len(possibleCars)
    
    def applyForce(Pvector):
    
        Pvector.f= Pvector.div(force,this.mass)
        acceleration.add(f)
      
    def update():
    
        velocity.add(acceleration)
        velocity.limit(maxspeed)
        location.add(velocity)
        acceleration.mult(0)
    
        stopIfCloseEnough()
        computePatience()
    
    def setInitDest(self, Path, ide):
        
        self.ide = int(ide)
                
        #unsigned long size = p.Destinations.size()
        #int ran = rand() % size
        longTermDest = p.Destinations[ide].get()
    
    #///////////////// Sub Functions ///////////////
    
    # Check the number of accident met during the trip 
    def checkNumOfAccidentMet():
    
        if(velocity.mag() != 0):
        
            NumAccidentMet+=1
        
    # Compute the patience of driver 
    def computePatience():
    
        patience = 1 - ((log10(localTime) / 4) * patient_time - (NumAccidentMet / 5) * patient_acci + possibleCars.size() * patient_cars)
    
        if(patience <= 0):
        
            patience = 0
        
        elif (patience >= 1):
        
            patience = 1
    
    # Make the vehicle completely stoped if crashed 
    def ifCrashed(pVector):
    
        if(crashed == true):
        
            Pvector.breakForce = Pvector.mult(velocity, -1)
            acceleration.multiply(0)
            applyForce(breakForce)
        
    # Stop the car if it is very close to goal, and reset counter back to zero, so that next behavior can be carried out 
    def stopIfCloseEnough():
    
        approach = float(Pvector.dist(this.goal, this.location))
    
        if(approach < 1):
            (this.location) = (this.goal)
            this.counter = 0
        
    # Return true only if the previous behaior is finished (i.e. counter = 0) 
    def setGoal():
        
        yesOrNo == true
    
        if(this.counter > 0):
            yesOrNo == false
        
        return yesOrNo
    
    # Return true if the car has reached the goal (i.e. at the "out" point) 
    def isArrived():
        
        if(this.location.x == this.goal.x & this.location.y == this.goal.y & this.goal.inOrOut == 0):
            return true
        else:
            return false
    
    # Return true if the car has reached the goal (i.e. at the "in" point) 
    def aboutToGo():
        if(this.location.x == this.goal.x & this.location.y == this.goal.y & this.goal.inOrOut == 1):
            return true
        else:
            return false
    
    # Return true if the point asked is accessible ( p->mainJunctions[argument1]->subJunctions[argument2]->accessible ) 
    def isAccessible(self,Path, i, j):
        
        self.i = float(i)
        self.j = float(j)
        
        if (p.mainJunctions[i].subJunctions[j].accessible == 1):
            return true
        else:
            return false
         
    # Return true if the point asked is In or Out ( p->mainJunctions[argument1]->subJunctions[argument2]->argument3 ) 
    def isInOrOut(self, Path, i, j, in_or_out):
        
        self.i = float(i)
        self.j = float(j)
        self.in_or_out = null
        
        if (p.mainJunctions[i].subJunctions[j].inOrOut == in_or_out):
            return true
        else:
            return false
        
    def map(self, d, ilb, iub, olb, oub):
        
        self.d = float(d)
        self.ilb = float(ilb)
        self.iub = float(iub)
        self.olb = float(olb)
        self.oub = float(oub)
    
        return (((oub-olb)*d)/(iub-ilb))