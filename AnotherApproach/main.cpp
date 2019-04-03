/*****************************************************************
 * Project:     Traffic Simulation through Agent-based Modelling
 *
 * Lecture:     System & Self-Organization
 *              Sommer Semester 2017, Hochschule Rhein-Waal
 *
 * Objective:   This project demonstrates the emergent behavior
 *              that takes place among a group of drivers travelling
 *              in a pre-defined map. The traffic flow depends not
 *              only on the number of agents in the city, but also
 *              the interaction between them. The behavior of one
 *              driver is influenced by other drivers on the street
 *              as well as other factors like traffic jam. An overall
 *              emergent effect is thereby generated and is observable.
 *
 * Author:      Yu-Jeng Kuo, Arindam Mahanta, Anoshan Indreswaran
 *
 * Last update: 21.07.2017
 ******************************************************************/


#include "dialog.h"
#include <QApplication>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Dialog w;
    w.show();

    return a.exec();
}
