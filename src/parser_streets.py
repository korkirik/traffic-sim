import json

from streetsegment import *
from geomap import Converter
    #Should extract data from OSM, create a temp object and fill the fields in it,
    # when everything is filled parser should pass object into street_segment_list

class Parser:
    def __init__(self):
        self.street_segment_list = list()

    def parse_file(self, file_name):

        with open(file_name, 'r') as export:
            meta_data = json.load(export)
        number_of_elements = len(meta_data['features'])

        print('Parsing file {}'.format(file_name))
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

                    street = StreetSegment(Pvector(startXcoor,startYcoor),
                    Pvector(endXcoor,endYcoor))

                    street.name = self.name
                    street.streetType = self.highway
                    street.lanes = self.lanes
                    street.lanesForward = self.fwdlanes
                    street.lanesBackward = self.bcklanes
                    street.speed = self.speed


                    self.street_segment_list.append(street)


        export.close()
        print('Done')

    def get_street_segment_list(self):
        return self.street_segment_list

    def convert_to_mercator_coordinates(self):
        c = Converter()
        for street in self.street_segment_list:
            street.start_point = c.convert_point(street.start_point.x, street.start_point.y)
            street.end_point = c.convert_point(street.end_point.x, street.end_point.y)
