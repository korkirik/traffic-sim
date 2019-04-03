/*****************************************************************
 *
 * Classname
 *  - DrunkDriver
 *
 * Brief
 *  - Implementation of drunk driving behavior
 *
 * Inherit
 *  - class Vehicle
 *
 * Virtual Function
 *  - void move()
 *    void makeTurn()
 *    void applyBehaviour()
 *    Pevctor* follow()
 *    Pevctor* separate()
 *
 * Detail
 *  - Implement its own behavior (drunk) by inheriting the
 *    decision-related functions from Vehicle class.
 *
 ******************************************************************/

#ifndef DRUNKDRIVER_H
#define DRUNKDRIVER_H
#include "vehicle.h"

class DrunkDriver : public Vehicle
{
public:
    DrunkDriver(float, float, int, float, Path*, unsigned long);

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* General function to describe the movement */
    void move(std::vector<Vehicle *> );

    /* Decide which junction points to choose */
    void makeTurn(Path*);

    /* Apply force on the agent */
    void applyBehaviour(std::vector<Vehicle*> );

    /* Follow the car in front of you */
    Pvector* follow();

    /* Separate from other cars*/
    Pvector* separate(std::vector<Vehicle *> );

    /* If someone is found, follow him, otherwise goToJunction */
    Pvector* arrive(std::vector<Vehicle *> );

};

#endif // DRUNKDRIVER_H
