#include "normaldriver.h"

NormalDriver::NormalDriver(float posX, float posY, int _id, float maxV, Path* p, unsigned long globalTime)
    : Vehicle(posX, posY, _id, maxV)
{
    //setInitDest(p);
    syncTime = globalTime;
}

void NormalDriver::move(std::vector<Vehicle *> vehicles)
{
    crashedInFront = false;

    applyBehaviour(vehicles);

    if(crashedInFront == true)
    {
        Pvector* breakForce = Pvector::mult(velocity, -1);
        acceleration->mult(0);
        applyForce(breakForce);

        checkNumOfAccidentMet();
    }

    ifCrashed();

    syncTime++;
    localTime++;
}

void NormalDriver::makeTurn(Path* p)
{
    /* is true if the car is arrived at the "drive out" point and ready to make turn */
    if(setGoal() && isArrived())
    {
        for(unsigned long i = 0; i < p->mainJunctions[tempGoal]->subJunctions.size(); i++)
        {
            /* check only the "drive in" points in this junction and if they are accesssible */
            if(isInOrOut(p, this->tempGoal, i, 1) && isAccessible(p, this->tempGoal, i))
            {
                JunctionPoint point = p->mainJunctions[tempGoal]->subJunctions[i]->get();

                /* randomly choose one junction points, and set it as goal */
                this->possibleDest.push_back(point);
            }
        }

        int options = this->possibleDest.size();
        int decision = rand() % options;

        *(this->goal) = this->possibleDest[decision].get();

        this->possibleDest.clear();

        goals.erase (goals.begin());
        goals.push_back(goal);

        this->counter += 1;
    }
}


Pvector* NormalDriver::arrive(std::vector<Vehicle *> vehicles)
{   
    Pvector *sum = new Pvector(0,0);

    /* Find if anyone is in front of me */
    findSomeoneInFront(vehicles);

    if(followSomeone == false && goal->inOrOut == 0)
    {
        for(unsigned long i = 0; i < possibleCars.size(); i++)
        {
            float sameGoal = Pvector::dist(goal, possibleCars[i]->goal);
            float tempD = 10000;

            if(sameGoal == 0 && possibleCars[i]->goal->inOrOut == goal->inOrOut)
            {
                float myDistToThere = Pvector::dist(goal, location);
                float hisDistToThere = Pvector::dist(possibleCars[i]->goal, possibleCars[i]->location);

                float distToHim = Pvector::dist(possibleCars[i]->location, location);

                if(hisDistToThere < myDistToThere && distToHim < tempD)
                {
                    followSomeone = true;
                    whoIfollowed = i;
                    tempD = distToHim;
                }
            }
        }
    }


    if(followSomeone == true && goal->inOrOut == 0)
    {
        /* check the distance and the guy driving ahead */
        float distToSomeone = Pvector::dist( possibleCars[whoIfollowed]->location, location);

        /* Stay where i am at the moment i find him */
        if(velocity->mag() != 0)
        {
            *mySteerForce = velocity->get();
            mySteerForce->mult(-1);
            sum = mySteerForce;

        }
        /* Wait and do nothing until someone in front is already 30 pixel away */
        else if(distToSomeone < 20){

        }
        /* Cannot not find anyone to follow? okay, then go where you planned to go */
        else
        {
            sum = goToJunction();
        }
    }
    else
    {
        sum = goToJunction();
    }

    possibleCars.clear();
    return sum;
}

Pvector * NormalDriver::goToJunction()
{
    Pvector *desired = Pvector::sub(this->goal, this->location);

    float d = desired->mag();
    desired->normalize();

    if(d < 100)
    {
        float m= map(d, 0, 100, 0, maxspeed);
        desired->mult(m);
    }
    else
    {
        desired->mult(maxspeed);
    }

    Pvector *steer = Pvector::sub(desired, this->velocity);
    steer->limit(maxforce);

    followSomeone = false;
    return steer;
}

Pvector* NormalDriver::separate(std::vector<Vehicle*> vehicles)
{
    float desiredSeperation = 10;
    int tooClosecount = 0;
    int radius = 50;
    Pvector *sum = new Pvector(0,0);

    for (std::vector<Vehicle*>::iterator it = vehicles.begin() ; it != vehicles.end(); ++it )
    {
        float d = Pvector::dist(location, (*it)->location);

        /* Calculate vector pointing to neighbor */
        Pvector *pointToSomeone = Pvector::sub( (*it)->location, location);
        Pvector *myDirection = Pvector::sub(goal, location);
        float angle = Pvector::angleBetween(myDirection, pointToSomeone);

        if (d < radius && d > 0 && crashed == false)
        {
            /* If distance to other vehicle is too close, then we assume they're crashed */
            if (d < 3)
            {
                crashed = true;
                numOfAcc = 1;
                memory = syncTime;
            }
            else if( d < 20 && angle < 20 && (*it)->crashed == true )
            {
                crashedInFront = true;
            }

            if (d < desiredSeperation)
            {
                Pvector *diff = Pvector::sub(location, (*it)->location);
                diff->normalize();
                diff->div(d);

                sum->add(diff);
                tooClosecount ++;
            }
        }
    }

    /* Average */

    if(tooClosecount > 0)
    {
        if(tooClosecount > 3 && tooClosecount < 7)     //  simulating a traffic jam
        {
            sum->div(tooClosecount);
            sum->setMag(0);
        }
        else {
            sum->div(tooClosecount);
            sum->setMag(maxspeed);
        }
    }

    if (sum->mag() > 0)
    {
        sum->setMag(maxspeed);
        sum->sub(velocity);
        sum->limit(maxforce);
    }

    /* returns the force vector to be applied */
    return sum;
}


Pvector* NormalDriver::follow()
{
    Pvector *here = new Pvector(0,0);
    *here = this->goals[myCurrentGoal]->get();

    float worldRecord = 1000000;

    Pvector *there = new Pvector(0,0);
    *there = this->goals[myCurrentGoal + 1]->get();
    Pvector *foll = new Pvector(0,0);

    Pvector predict = velocity->get();
    predict.normalize();
    predict.mult(25);
    Pvector *predictLoc = Pvector::add(location, &predict );

    //Single path

    Pvector *normalPoint = Pvector::getNormalPoint(predictLoc, here, there);

    if(normalPoint->x < fmin(here->x, there->x) || normalPoint->x > fmax(here->x, there->x))
    {
        *normalPoint = there->get();
    }
    else if(normalPoint->y < fmin(here->y, there->y) || normalPoint->y > fmax(here->y, there->y))
    {
        *normalPoint = there->get();
    }

    Pvector *dir = Pvector::sub(there, here);
    dir->normalize();
    dir->mult(10);
    Pvector *target = Pvector::add(normalPoint, dir);

    if (worldRecord > 5)
    {
        foll = seek(target);
    }

    /* returns the force required to follow a path */
    return foll;
}

void NormalDriver::applyBehaviour(std::vector<Vehicle*> vehicles)
{
    Pvector* sep = separate(vehicles);
    Pvector* arr = arrive(vehicles);
    Pvector* foll = follow();

    /* weight for seperate behaviour (high value will mean high consideration for *seperation*) */
    sep->mult(0.4);
    arr->mult(1);
    foll->mult(0.4);

    applyForce(sep);
    applyForce(arr);
    applyForce(foll);
}




