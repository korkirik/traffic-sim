'''
/*****************************************************************
 * Project:     Traffic Simulation through Agent-based Modelling
 *
 * Lecture:     System & Self-Organization
 *              Sommer Semester 2017, Hochschule Rhein-Waal
 *              &&
 *              Sommer Semester 2019, Hochschule Rhein-Waal
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
 *   Developed by: Yusuf Ismail, Kirill Korolev, Leen Nijim
 * Based on initial work of:
    Yu-Jeng Kuo, Arindam Mahanta, Anoshan Indreswaran
 ******************************************************************/
'''
from map import *
from parser_osm import *
from pseudoparser import *

#from array import *

map = Map()
psparser = PseudoParser()
psparser.parseFile()
map.loadStreets(psparser.getStreetSegmentList())
map.generateNodes()
map.drawStreets()
#simulation = Simulation()    To be added later!
