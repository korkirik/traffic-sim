#include "junction.h"

Junction::Junction(float x, float y)
{
    junLocation = new Pvector (x, y);
    addPoints(x, y);
    setStatus();
}


void Junction::addPoints(float x, float y)
{
    subJunctions.push_back( new JunctionPoint(x+20, y-10, 0));
    subJunctions.push_back( new JunctionPoint(x+10, y-20, 1));
    subJunctions.push_back( new JunctionPoint(x-10, y-20, 2));
    subJunctions.push_back( new JunctionPoint(x-20, y-10, 3));
    subJunctions.push_back( new JunctionPoint(x-20, y+10, 4));
    subJunctions.push_back( new JunctionPoint(x-10, y+20, 5));
    subJunctions.push_back( new JunctionPoint(x+10, y+20, 6));
    subJunctions.push_back( new JunctionPoint(x+20, y+10, 7));
}

void Junction::setStatus()
{
    /* Set junction points as IN or OUT */
    for(unsigned long i = 0; i < subJunctions.size(); i += 2)
    {
        subJunctions[i]->inOrOut = 0;
    }
    for(unsigned long i = 1; i < subJunctions.size(); i += 2)
    {
        subJunctions[i]->inOrOut = 1;
    }

    /* Set junction points as accessible or not */
    for(unsigned long i = 0; i < subJunctions.size(); i ++)
    {
        if(subJunctions[i]->x > 410 || subJunctions[i]->x < -410)
        {
            subJunctions[i]->accessible = false;
        }
        else if(subJunctions[i]->y > 410 || subJunctions[i]->y < -410)
        {
            subJunctions[i]->accessible = false;
        }
    }
}
