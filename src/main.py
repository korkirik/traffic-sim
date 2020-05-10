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
 * Based on ideas from the work of:
    Yu-Jeng Kuo, Arindam Mahanta, Anoshan Indreswaran
 ******************************************************************/
'''
from map import *
from parser_streets import *
from simulation import *

from pseudoparser_testground2 import *
from proving_ground import *

map = Map()
#psparser = Parser()
#psparser = ProvingGround()
psparser = PseudoParserTestground()
map.load_streets(psparser.get_street_segment_list())
map.generate_nodes()

map.save_map_to_file()
map.print_nodes_stats(0)

simulation = Simulation()
simulation.load_nodes(map.node_list)
simulation.create_roaming_agents(9)
simulation.start_simulation(1000)
