from map import *
from streets_parser import *
from simulation import *
from area import Area
from testing_maps import *

map = Map()
psparser = Parser()
psparser = WalkingMap()

map.load_streets(psparser.get_street_segment_list())
map.generate_nodes()
map.save_map_to_json()
map.print_nodes_stats(0)

simulation = Simulation()
simulation.load_nodes(map.get_node_list())

Area.set_all_node_list(list())
area = Area(0,0,1)
area2 = Area(0,0,1)
simulation.read()
area.set_test_coordinates(1,1,3)
area2.set_test_coordinates(5,2,4)

simulation.create_walker(50, area)
#simulation.create_roaming_walker(5, area2)
simulation.create_curiosities(25)
simulation.create_destinations(2)
simulation.start_simulation(1000)
