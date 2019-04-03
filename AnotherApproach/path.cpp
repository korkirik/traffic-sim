#include "path.h"

Path::Path(){

    // Initial junctions (smaller map)
    addMainJunctions(-200, 200);
    addMainJunctions(   0, 200);
    addMainJunctions( 200, 200);
    addMainJunctions( 200,   0);
    addMainJunctions( 200,-200);
    addMainJunctions(   0,-200);
    addMainJunctions(-200,-200);
    addMainJunctions(-200,   0);
    addMainJunctions(   0,   0);

    // Newly added junctions (Bigger map)
    addMainJunctions(-400,-400);
    addMainJunctions(-200,-400);
    addMainJunctions(   0,-400);
    addMainJunctions( 200,-400);
    addMainJunctions( 400,-400);
    addMainJunctions( 400,-200);
    addMainJunctions( 400,   0);
    addMainJunctions( 400, 200);
    addMainJunctions(-400,-200);
    addMainJunctions(-400,   0);
    addMainJunctions(-400, 200);
    addMainJunctions(-400, 400);
    addMainJunctions(-200, 400);
    addMainJunctions(   0, 400);
    addMainJunctions( 200, 400);
    addMainJunctions( 400, 400);

    Destinations.push_back(new Pvector( 380, 380));
    Destinations.push_back(new Pvector( 120,-380));
    Destinations.push_back(new Pvector(-320, 220));
    Destinations.push_back(new Pvector(  80,  20));

}

void Path::addMainJunctions(float x, float y)
{
    mainJunctions.push_back(new Junction(x,y));
}
