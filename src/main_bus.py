from map import *
from streets_parser import *
from simulation_bus import *
from area import Area

from testing_maps import *

map = Map()
psparser = Parser()
psparser.parse_file('map2.geojson')
psparser.convert_to_mercator_coordinates()  #required for agents running on osm map

map.load_streets(psparser.get_street_segment_list())
map.generate_nodes()

map.save_map_to_json()
map.print_nodes_stats(0)

simulation = Simulation()
simulation.load_nodes(map.get_node_list())
simulation.add_bus_stops()

Area.set_all_node_list(list())

simulation.create_homing_agents(1, 'bus')
simulation.start_simulation(5500)
