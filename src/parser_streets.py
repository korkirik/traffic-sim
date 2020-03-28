import json

from parser_osm import Parser
from streetsegment import *

    #Should extract data from OSM, create a temp object and fill the fields in it,
    # when everything is filled parser should pass object into streetSegmentList

class Parser
    def __init__(self):
            self.streetSegmentList = list()

            with open('export_map_data_smaller.json', 'r') as export: #&&&&
                meta_data = json.load(export)
            number_of_elements = len(meta_data['features'])

            for i in range(0, number_of_elements):
                geometry = meta_data['features'][i]['geometry']
                if geometry['type'] == 'LineString':
                    properties = meta_data['features'][i]['properties']

                    self.highway = properties.get('highway','Street')

                    self.name = properties.get('name','Street name')

                    self.lanes = int(properties.get('lanes','1'))

                    self.speed = int(properties.get('maxspeed','50'))

                    if self.lanes > 2:
                        self.bcklanes = int(properties.get('lanes:backward','1'))
                        self.fwdlanes = int(properties.get('lanes:forward','1'))
                    else: #defaults
                        self.fwdlanes = 1
                        self.bcklanes = 1

                    segments = len(geometry['coordinates']) -1

                    for segment in range(0, segments):

                        startXcoor = geometry['coordinates'][segment][0]

                        startYcoor = geometry['coordinates'][segment][1]

                        endXcoor = geometry['coordinates'][segment +1][0]

                        endYcoor = geometry['coordinates'][segment +1][1]

                        StrSeg = StreetSegment(Pvector(startXcoor,startYcoor),
                        Pvector(endXcoor,endYcoor))

                        StrSeg.name = self.name
                        StrSeg.streetType = self.highway
                        StrSeg.lanes = self.lanes
                        StrSeg.lanesForward = self.fwdlanes
                        StrSeg.lanesBackward = self.bcklanes
                        StrSeg.speed = self.speed


                        self.streetSegmentList.append(StrSeg)


            export.close()

            def getStreetSegmentList(self):
                return self.streetSegmentList
