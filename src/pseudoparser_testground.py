import random
from parser_streets import Parser
from streetsegment import *

class PseudoParserTestground(Parser):
    def __init__(self):
            self.street_segment_list = list()
            self.getData()

    def getData(self):
        street1 = StreetSegment(Pvector(0,0), Pvector(5,2))
        street2 = StreetSegment(Pvector(5,2), Pvector(12,-1))
        street3 = StreetSegment(Pvector(12,-1), Pvector(16,2))
        street4 = StreetSegment(Pvector(12,-1), Pvector(15,-5))

        self.street_segment_list.append(street1)
        self.street_segment_list.append(street2)
        self.street_segment_list.append(street3)
        self.street_segment_list.append(street4)

    def get_street_segment_list(self):
        return self.street_segment_list
