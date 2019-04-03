/*****************************************************************
 *
 * Classname
 *  - Pvector
 *
 * Brief
 *  - A toolbox that manipulate all the physics behind the simulation
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - Pvector class contains all the necessary tools for doing maths
 *    on a two-dimensional vector space. Most of the functions here
 *    are used in the Vehicles class to calculate the force in order
 *    to generate ideal forces to drive the agents.
 *
 ******************************************************************/
#ifndef PVECTOR_H
#define PVECTOR_H
#include "math.h"



class Pvector
{
public:
    Pvector(float, float);

    /*****************************************************************
                         Variable Declearation
     ******************************************************************/

    /* Coordinates x */
    float x;

    /* Coordinates y */
    float y;

    /*****************************************************************
                         Function Declearation
     ******************************************************************/

    /* Coordinates addition */
    void add(Pvector*);

    /* Coordinates subtraction */
    void sub(Pvector*);

    /* Coordinates multiplication */
    void mult(float);

    /* Coordinates division */
    void div(float);

    /* Normalize the magnitude of a vector to 1  */
    void normalize();

    /* Multiply the magnitude of a vector by x  */
    void setMag(float);

    /* Limit the magnitude of a vector  */
    void limit(float max);

    /* Return the magnitude of a vector  */
    float mag();

    /* Retuen the coordinates  */
    Pvector get();

    /*****************************************************************
                         Function Declearation (Static)
     ******************************************************************/
    /* Coordinates addition */
    static Pvector* add(Pvector*,Pvector*);

    /* Coordinates subtraction */
    static Pvector* sub(Pvector*,Pvector*);

    /* Coordinates multiplication */
    static Pvector* mult(Pvector*,float);

    /* Coordinates division */
    static Pvector* div(Pvector*,float);

    /* return the point projected by other vector (Dot product) */
    static Pvector* getNormalPoint(Pvector*, Pvector*, Pvector*);

    /* Return the dot product */
    static float dot(Pvector*, Pvector*);

    /* Return the angle between two vectors */
    static float angleBetween(Pvector*, Pvector*);

    /* Return the distance between two coordinates */
    static float dist(Pvector*, Pvector*);
};

#endif // PVECTOR_H
