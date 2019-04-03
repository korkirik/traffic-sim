/*****************************************************************
 *
 * Classname
 *  - Vehicle
 *
 * Brief
 *  - A class that manage everything about the vehicles
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  -
 *  void move()
 *  void applyBehaviour()
 *  void findSomeoneInFront()
 *  Pvector* arrive()
 *  Pvector* goToJunction()
 *  Pvector* follow()
 *  Pvector* separate()
 *  Pvector* seek()
 *  void makeTurn()
 *
 * Detail
 *  - Vehicle class contains all the member variables and member
 *    functions, which controls the movement, charateristics.
 *
 ******************************************************************/
#ifndef VEHICLE_H
#define VEHICLE_H
#include "pvector.h"
#include "path.h"
#include "stdlib.h"
#include "time.h"
#include <vector>

class Vehicle
{
public:

    Vehicle(float, float, int, float);

    /*****************************************************************
                         Variable Declearation
     ******************************************************************/

    /* Vector that stores the location of a vehicle */
    Pvector *location;

    /* Vector that represents the velocity of a vehicle */
    Pvector *velocity;

    /* Vector that represents the acceleration of a vehicle */
    Pvector *acceleration;

    /* Vector that stores the force acting on itself */
    Pvector *mySteerForce;

    /* Vector that stores the location of short-term goal (Junction point to Junction point) */
    JunctionPoint *goal;

    /* Vector that stores the location of long-term goal */
    Pvector* longTermDest;

    /* Maximum speed in integer */
    float maxspeed;

    /* Maximum force in integer */
    float maxforce;

    /* Weighted value for separation force */
    float sepWeight;

    /* Weighted value for following force */
    float folWeight;

    /* Weighted value for arriving force */
    float arrWeight;

    /* How patient one is with respect to time */
    float patient_time;

    /* How patient one is with respect to accident met */
    float patient_acci;

    /* How patient one is with respect to number of cars around */
    float patient_cars;

    /* Mass of the car */
    float mass;

    /* It's a function of time, accident encountered...etc. and influences the driving behavior */
    float patience;

    /* ID of the car, indexed by the order of generation */
    int id;

    /* Counter that makes sure the function will be run once */
    int counter;

    /* Remember the global time when crashed */
    int memory;

    /* Remember the number of cars around */
    int carsAroundMe;

    /* Number of Accident met */
    int NumAccidentMet;
    int numOfAcc;

    /* Counter that makes sure the function will be only run once */
    int onlyOnce;

    /* An integer that stores the index of an array */
    int myCurrentGoal;

    /* Check whether the car is following someone */
    bool followSomeone;

    /* Check whether the car has reached the destination */
    bool reachedDest;

    /* Check whether the car is crashed */
    bool crashed;

    /* Check whether there is an accident */
    bool crashedInFront;

    /* A clock that synchronized with the global time */
    unsigned long syncTime;

    /* Store the time taken to reach the destination */
    unsigned long localTime;

    /* Store the value from localTime, it's used for writing data */
    unsigned long lot;

    /* An index to store the temp choice in an array */
    unsigned long tempGoal;

    /* An index to store the temp choice in an array */
    unsigned long tempVar;

    /* An index to store the temp choice in an array */
    unsigned long whoIfollowed;

    /* A vector to store the possible destinations to choose from */
    std::vector<JunctionPoint> possibleDest;

    /* A vector to store the possible cars to search from */
    std::vector<Vehicle*> possibleCars;

    /* A vector to store the possible goals to reach to */
    std::vector<Pvector*> goals;

    /*****************************************************************
                     Function Declearation (Normal)
     ******************************************************************/

    /* Scan and choose which main junction to go to */
    void chooseJunction(Path*);

    /* Apply force on to agent */
    void applyForce(Pvector*);

    /* Update agent's position */
    void update();

    /* Set agent directly to the goal if it's very close */
    void stopIfCloseEnough();

    /* Set Initial Destination for some agents */
    void setInitDest(Path*, int);

    /* Check if vehicles is crashed */
    void ifCrashed();

    /* Computer the patience of driver */
    void computePatience();

    /* Update number of accident met */
    void checkNumOfAccidentMet();

    /* Map one input from range A to range B */
    float map(float, float, float, float, float);

    /* Check if current short-term goal is set */
    bool setGoal();

    /* Check if agent is coming "out" from the street */
    bool isArrived();

    /* Check if agent is driving "in" to the street */
    bool aboutToGo();

    /* Check if junction point is accessible */
    bool isAccessible(Path* , unsigned long, unsigned long);

    /* Check if junction point is "in" or "out" */
    bool isInOrOut(Path*, unsigned long, unsigned long, bool);


    /*****************************************************************
                     Function Declearation (Virtual)
     ******************************************************************/
    /* General function to describe the movement */
    virtual void move(std::vector<Vehicle* > ) = 0;

    /* Apply force on the agent */
    virtual void applyBehaviour(std::vector<Vehicle* >) = 0;

    /* If someone is found, follow him, otherwise goToJunction */
    virtual Pvector* arrive(std::vector<Vehicle* >);

    /* Get attracted to junction*/
    virtual Pvector* goToJunction();

    /* Follow the car in front of you */
    virtual Pvector* follow();

    /* Search if any cars is in the field of view */
    virtual void findSomeoneInFront(std::vector<Vehicle* >);

    /* Separate from other cars */
    virtual Pvector* separate(std::vector<Vehicle* >);

    /* Get attracted to the target */
    virtual Pvector* seek(Pvector*);

    /* Decide which junction points to choose */
    virtual void makeTurn(Path*);

};

#endif // VEHICLE_H
