/*****************************************************************
 *
 * Classname
 *  - Junction
 *
 * Brief
 *  - A class that resembles a crossroad in the map.
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A Junction is like a crossroad in the real world, ususally is
 *    the place where 4 streets come across. One junction contains
 *    basically 8 junction points, from which each pair represents
 *    driving "in" and "out" of the street.
 *
 ******************************************************************/
#ifndef JUNCTION_H
#define JUNCTION_H
#include "junctionpoint.h"
#include <vector>

class Junction
{
public:
    Junction(float, float);

    /*****************************************************************
                         Variable Declearation
     ******************************************************************/

    /* Where the center of the junction is located */
    Pvector* junLocation;

    /* A vector of 8 junction points at one crossroad, including 4 in and 4 out */
    std::vector<JunctionPoint*> subJunctions;

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* Add points to the junction ( 8 junction points will be added by calling it once ) */
    void addPoints(float, float);

    /* Filter out the points where no further connection is possible, and set up "in" and "out" points */
    void setStatus();

};

#endif // JUNCTION_H
