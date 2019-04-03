#include "pvector.h"

Pvector::Pvector(float _x, float _y)
{
    x = _x;
    y = _y;
}

void Pvector::add(Pvector *velo){
    x += velo->x;
    y += velo->y;
}

void Pvector::sub(Pvector *velo){
    x += velo->x;
    y += velo->y;
}

void Pvector::mult(float n){
    this->x *= n;
    this->y *= n;
}

void Pvector::div(float n){
    this->x /= n;
    this->y /= n;
}

float Pvector::mag(){
    return sqrtf(this->x*this->x + this->y*this->y);
}

void Pvector::normalize(){
    float m = mag();
    if(m != 0){
        div(m);
    }
}

Pvector Pvector::get(){
    Pvector *v1 = new Pvector(0,0);
    *v1 = *this;
    return *v1;
}

void Pvector::setMag(float x)
{
    this->normalize();
    this->mult(x);
}


void Pvector::limit(float max){
    if (this->mag() > max)
    {
        this->setMag(max);
    }
}

Pvector* Pvector::add(Pvector* v1,Pvector* v2){
    Pvector* v3 = new Pvector(v1->x + v2->x, v1->y + v2->y);
    return v3;
}

Pvector* Pvector::sub(Pvector* v1,Pvector* v2){
    Pvector* v3 = new Pvector(v1->x - v2->x, v1->y - v2->y);
    return v3;
}

Pvector* Pvector::mult(Pvector* v1, float n){
    Pvector *v3 = new Pvector(v1->x* n ,v1->y* n);
    return v3;
}

Pvector* Pvector::div(Pvector* v1,float n){
    Pvector *v3 = new Pvector(v1->x/ n ,v1->y/ n);
    return v3;
}

float Pvector::dot(Pvector* v1, Pvector* v2){
   return (v1->x*v2->x) + (v1->y*v2->y);
}

float Pvector::angleBetween(Pvector* v1, Pvector* v2)
{
   float theta = acosf(dot(v1,v2)/(v1->mag()*v2->mag()));
   return theta;
}

Pvector* Pvector::getNormalPoint(Pvector* p, Pvector* a, Pvector* b){
    Pvector *ap = sub(p,a);
    Pvector *ab = sub(b,a);

    ab->normalize();
    ab->mult(dot(ap,ab));

    Pvector* normalPoint = add(a,ab);

    return normalPoint;
}

float Pvector::dist(Pvector* a, Pvector* b){
    return sqrt(((a->x)-(b->x))*((a->x)-(b->x)) + ((a->y)-(b->y))*((a->y)-(b->y)));
}
