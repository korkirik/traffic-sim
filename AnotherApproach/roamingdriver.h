/*****************************************************************
 *
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
 *
 ******************************************************************/
#ifndef ROAMINGDRIVER_H
#define ROAMINGDRIVER_H
#include "vehicle.h"

class RoamingDriver:public Vehicle
{
public:
    RoamingDriver(float, float, int, float);

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* General function to describe the movement */
    void move(std::vector<Vehicle *> );

    /* Apply force on the agent */
    void applyBehaviour(std::vector<Vehicle*> vehicles);
};

#endif // ROAMINGDRIVER_H
