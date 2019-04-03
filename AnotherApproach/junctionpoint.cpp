#include "junctionpoint.h"

JunctionPoint::JunctionPoint(float x, float y, int i)
    :Pvector(x,y)
{
    accessible = true;
    inOrOut = true;
    index = i;
}

JunctionPoint JunctionPoint::get(){
    JunctionPoint *v1 = new JunctionPoint(0,0,0);
    *v1 = *this;
    return *v1;
}
