/*****************************************************************
 *
 * Classname
 *  - NormalDriver
 *
 * Brief
 *  - Implementation of normal driving behavior
 *
 * Inherit
 *  - class Vehicle
 *
 * Virtual Function
 *  - void move()
 *    void makeTurn()
 *    void applyBehaviour()
 *    void findSomeoneInFront()
 *    Pevctor* follow()
 *    Pevctor* separate()
 *
 * Detail
 *  - Implement its own behavior (Normal) by inheriting the
 *    decision-related functions from Vehicle class.
 *
 ******************************************************************/
#ifndef NORMALDRIVER_H
#define NORMALDRIVER_H
#include "vehicle.h"

class NormalDriver : public Vehicle
{
public:
    NormalDriver(float, float, int, float, Path*, unsigned long);

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* General function to describe the movement */
    void move(std::vector<Vehicle *> );

    /* Decide which junction points to choose */
    void makeTurn(Path*);

    /* Apply force on the agent */
    void applyBehaviour(std::vector<Vehicle*> );

    /* If someone is found, follow him, otherwise goToJunction */
    Pvector* arrive(std::vector<Vehicle*> );

    /* Get attracted to junction*/
    Pvector* goToJunction();

    /* Separate from other cars */
    Pvector* separate(std::vector<Vehicle*> );

    /* Follow the car in front of you */
    Pvector* follow();


};

#endif // NORMALDRIVER_H
