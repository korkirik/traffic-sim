/*****************************************************************
 *
 * Classname
 *  - JunctionPoint
 *
 * Brief
 *  - A class that resembles driving "in" or "out" a street
 *
 * Inherit
 *  - class Pvector
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A Junction point is like the entrance or exit of the street.
 *    As this class inherits from the Pvector class, each junction
 *    points has its own coordinates. In addition, it also carries
 *    other infomation like accessibility, direction (in or out)...etc.
 *
 ******************************************************************/
#ifndef JUNCTIONPOINT_H
#define JUNCTIONPOINT_H
#include "pvector.h"


class JunctionPoint: public Pvector
{
public:

    JunctionPoint(float,float,int);

    /*****************************************************************
                         Variable Declearation
     ******************************************************************/

    /* If this junction point can take you to next junction, it's accessible. Otherwise, it's not (e.g. at the corner) */
    bool accessible;

    /* A street has only two ends, one is to drive in, the other is to drive out */
    bool inOrOut;

    /* It's used to record the relative position of the junction points at the junction */
    int index;


    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* Return a junction point object */
    JunctionPoint get();

};

#endif // JUNCTIONPOINT_H
