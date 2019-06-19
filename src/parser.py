import json

from parser_osm import Parser
from streetsegment import *
with open('export_map_data.json', 'r') as export:
    meta_data = json.load(export)


class LParser(Parser):
    def __init__(self):
            self.streetSegmentList = list()
            number_of_elements = len(meta_data['features'])

            for i in range(0, number_of_elements):
                geometry = meta_data['features'][i]['geometry']
                if geometry['type'] == 'LineString':
                    properties = meta_data['features'][i]['properties']

                    highway = properties.get('highway','Street')
                    #print(type(highway))
                    #print(highway)
                    name = properties.get('name','Street name')

                    #print(name)
                    lanes = int(properties.get('lanes','1'))

                    #print(lanes)
                    #print(type(lanes))
                   # print("\n")

                    segments = len(geometry['coordinates']) -1
                    #print(segments)
                    #print(type(segments))

                    for segment in range(0, segments):
                        print(name)
                        print(highway)
                        print(lanes)

                        startXcoor = geometry['coordinates'][segment][0]
                        print(startXcoor)
                        #print(type(startXcoor))

                        startYcoor = geometry['coordinates'][segment][1]
                        print(startYcoor)
                        #print(type(startYcoor))

                        endXcoor = geometry['coordinates'][segment +1][0]
                        print(endXcoor)
                        #print(type(endXcoor))

                        endYcoor = geometry['coordinates'][segment +1][1]
                        print(endYcoor)
                        #print(type(endYcoor))

                        print('\n')


            export.close()