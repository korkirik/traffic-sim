/*****************************************************************
 *
 * Classname
 *  - Dialog
 *
 * Brief
 *  - An interface between Qt and user.
 *
 * Inherit
 *  - None
 *
 * Virtual Function
 *  - None
 *
 * Detail
 *  - The main body of simulation. It's where the programmer
 *    controls and displays the vehicles. One important function
 *    named "theLoop" is the body of the simulation, responsible
 *    for updating the simulation frame by frame.
 *
 ******************************************************************/

#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QtCore>
#include <QtGui>
#include <QGraphicsScene>
#include "drunkdriver.h"
#include "normaldriver.h"
#include "path.h"
#include "junction.h"

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();

private:

/*****************************************************************
                       System Declearation
 ******************************************************************/
    Ui::Dialog *ui;
    QGraphicsScene *scene;
    QTimer *timer;

/*****************************************************************
                     Variable Declearation
 ******************************************************************/

    /* A vector that contains all the vehicles*/
    std::vector<Vehicle*> vehicles;

    /* A map contains 9 junctions, each junction contains 8 junctions points */
    Path *p;

/*****************************************************************
                      Function Declearation
******************************************************************/
private slots:

    /* A main function that updates every other functions */
    void theLoop();

    /* Update the agent bahavior and position */
    void run(std::vector<Vehicle *> &, Path* );

    /* Add experimental driver into simulation */
    void addExperiDriver(unsigned long, unsigned long);

    /* Display the streets */
    void drawMap(QPen,QPen);

    /* Display the cars */
    void drawCars(std::vector<Vehicle*> & , QPen , QPen  , QPen , QPen, QPen);

    /* Display the long-term destination */
    void drawDest(Path*, QPen);

    /* Display Junctions */
    void showJunctions(Path*, QPen, QPen);

    /* Stop/Start the simulation */
    void on_pushButton_clicked();

    /* Adjust the simulation speed */
    void on_verticalSlider_valueChanged(int);

    /* Stop Simulatioj at desired iteration */
    void stopSimulation(unsigned long);

    /* Write data to external file (sorted by ID) */
    void writeDataVel(std::vector<Vehicle *> &, QString , QString, int );

    /* Write data to external file (Get everything) */
    void writeData(std::vector<Vehicle *> &, QString , QString );


};

#endif // DIALOG_H
