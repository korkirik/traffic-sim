/*****************************************************************
 *
 * Classname
 *  - Path
 *
 * Brief
 *  - A class that resembles the whole map
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - A path is like the whole map where agents are travelling.
 *    A path object manages all the main junctions, and it also stores
 *    where the final destination are.
 *
 ******************************************************************/
#ifndef PATH_H
#define PATH_H
#include "pvector.h"
#include "junction.h"
#include <vector>

class Path
{
public:
    Path();

    /*****************************************************************
                         Variable Declearation
     ******************************************************************/

    /* A vector that stores the coordinates of some destinations*/
    std::vector<Pvector*> Destinations;

    /* A vector that manages all the junctions*/
    std::vector<Junction*> mainJunctions;

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* Add junction on to the map */
    void addMainJunctions(float, float);

};

#endif // PATH_H
