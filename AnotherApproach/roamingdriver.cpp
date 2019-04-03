#include "roamingdriver.h"

RoamingDriver::RoamingDriver(float posX, float posY, int _id, float maxV)
    : Vehicle(posX, posY, _id, maxV)
{

}

void RoamingDriver::move(std::vector<Vehicle *> vehicles){

    applyBehaviour(vehicles);
}

void RoamingDriver::applyBehaviour(std::vector<Vehicle*> vehicles)
{
    //Pvector* sep = separate(vehicles);
    Pvector* arr = arrive(vehicles);
    Pvector* foll = follow();

    foll->mult(0.2);
    //sep->mult(1);
    arr->mult(1);

    //applyForce(sep);
    applyForce(foll);
    applyForce(arr);

}
