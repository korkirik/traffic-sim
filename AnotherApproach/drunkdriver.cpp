#include "drunkdriver.h"

DrunkDriver::DrunkDriver(float posX, float posY, int _id, float maxV, Path* p, unsigned long globalTime)
    : Vehicle(posX, posY, _id, maxV)
{
    setInitDest(p, _id );
    syncTime = globalTime;
}

void DrunkDriver::move(std::vector<Vehicle *> vehicles)
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

    float tmpDist = Pvector::dist(location, longTermDest);

    if( tmpDist < 20 )
    {
        reachedDest = true;
        lot = localTime;
    }

    if(reachedDest != true)
    {
        syncTime++;
        localTime++;
    }
}

void DrunkDriver::makeTurn(Path* p)
{
    /* Is true if the car is arrived at the "drive out" point and ready to make turn */
    if(setGoal() && isArrived())
    {
        for(unsigned long i = 0; i < p->mainJunctions[tempGoal]->subJunctions.size(); i++)
        {
            /* check only the "drive in" points in this junction and if they are accesssible */
            if(isInOrOut(p, this->tempGoal, i, 1) && isAccessible(p, this->tempGoal, i)){

                JunctionPoint point = p->mainJunctions[tempGoal]->subJunctions[i]->get();

                /* randomly choose one junction points, and set it as goal */
                this->possibleDest.push_back(point);
            }
        }
        unsigned long options = this->possibleDest.size();

        Pvector* destVec = Pvector::sub(longTermDest, goal);

        int tempChoice = 0;
        float tempAngle = 1800;

        for(unsigned long i = 0; i < options; i++)
        {
            Pvector* tmpVec = Pvector::sub(&possibleDest[i], goal);
            float angle = Pvector::angleBetween(destVec, tmpVec);

            if(angle < tempAngle)
            {
                tempAngle = angle;
                tempChoice = i;
            }
        }
        *(this->goal) = this->possibleDest[tempChoice].get();

        this->possibleDest.clear();

        goals.erase (goals.begin());
        goals.push_back(goal);

        this->counter += 1;
    }
}

Pvector* DrunkDriver::follow()
{
    Pvector *here = new Pvector(0,0);
    *here = this->goals[myCurrentGoal]->get();

    Pvector *there = new Pvector(0,0);
    *there = this->goals[myCurrentGoal + 1]->get();

    float worldRecord = 1000000;
    Pvector *foll =  new Pvector(0,0);

    Pvector predict = velocity->get();
    predict.normalize();
    predict.mult(25);
    Pvector *predictLoc = Pvector::add(location, &predict );

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

    /* 5 is the path radius */
    if (worldRecord > 5)
    {
        foll = seek(target);
    }

    return foll;
}

Pvector* DrunkDriver::separate(std::vector<Vehicle*> vehicles)
{
    /* 5 = radius of car object */
    float desiredSeperation = 10 * 2;
    int tooClosecount = 0;
    int radius = 50;
    Pvector *sum = new Pvector(0,0);

    for (std::vector<Vehicle*>::iterator it = vehicles.begin() ; it != vehicles.end(); ++it )
    {
        float d = Pvector::dist(location, (*it)->location);

        /* Calculate vector pointing to neighbor */
        Pvector *pointToSomeone = Pvector::sub( (*it)->location, location );
        Pvector *myDirection = Pvector::sub(goal, location);
        float angle = Pvector::angleBetween(myDirection, pointToSomeone );

        if (d < radius && d > 0 && crashed == false)
        {
            /* If distance to other vehicle is too close, then it must have been crashed. */
            if (d < 3 && localTime > 200)
            {
                crashed = true;
                numOfAcc = 1;
                memory = syncTime;
                lot = 0;
            }
            else if( d < 20 && angle < 20 && (*it)->crashed == true)
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
        /* simulating a traffic jam */
        if(tooClosecount > 3 && tooClosecount < 7)
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
    return sum;

}

Pvector* DrunkDriver::arrive(std::vector<Vehicle *> vehicles)
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
        else if(distToSomeone < 30)
        {
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

void DrunkDriver::applyBehaviour(std::vector<Vehicle*> vehicles)
{
    Pvector* sep = separate(vehicles);
    Pvector* arr = arrive(vehicles);
    Pvector* foll = follow();

    sepWeight = 1 *patience;
    arrWeight = 1;
    folWeight = 1 / patience;

    /* weight for seperate behaviour (high value will mean high consideration for *seperation*) */
    sep->mult(sepWeight);
    arr->mult(arrWeight);
    foll->mult(folWeight);

    applyForce(sep);
    applyForce(arr);
    applyForce(foll);
}


