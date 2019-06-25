import json

from parser_osm import Parser
from streetsegment import *



class LParser(Parser):
    def __init__(self):
            self.streetSegmentList = list()
            with open('export_map_data.json', 'r') as export: #&&&&
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


                    segments = len(geometry['coordinates']) -1

                    for segment in range(0, segments):

                        self.startXcoor = geometry['coordinates'][segment][0]

                        self.startYcoor = geometry['coordinates'][segment][1]

                        self.endXcoor = geometry['coordinates'][segment +1][0]

                        self.endYcoor = geometry['coordinates'][segment +1][1]

                        self.StrSeg = StreetSegment(Pvector(self.startXcoor,self.startYcoor),Pvector(self.endXcoor,self.endYcoor))

                        self.StrSeg.name = self.name
                        self.StrSeg.streetType = self.highway
                        self.StrSeg.lanes = self.lanes
                        self.StrSeg.lanesForward = self.fwdlanes
                        self.StrSeg.lanesBackward = self.bcklanes
                        self.StrSeg.speed = self.speed


                        self.streetSegmentList.append(StrSeg)


            export.close()

            def getStreetSegmentList(self):
                return self.streetSegmentList
