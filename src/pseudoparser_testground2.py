import random
from parser_streets import Parser
from streetsegment import *

class PseudoParserTestground(Parser):
    def __init__(self):
            self.street_segment_list = list()
            self.get_data()

    def get_data(self):
        street1 = StreetSegment(Pvector(0,0), Pvector(5,2))
        street2 = StreetSegment(Pvector(5,2), Pvector(12,-1))
        street3 = StreetSegment(Pvector(12,-1), Pvector(16,2))
        street4 = StreetSegment(Pvector(12,-1), Pvector(15,-5))
        street5 = StreetSegment(Pvector(15,-5), Pvector(12,-10))
        street6 = StreetSegment(Pvector(12,-10), Pvector(5,-8))
        street7 = StreetSegment(Pvector(1,-6), Pvector(5,-8))
        street8 = StreetSegment(Pvector(0,0), Pvector(1,-6))
        street9 = StreetSegment(Pvector(5,2), Pvector(4,-3))
        street10 = StreetSegment(Pvector(0,0),Pvector(4,-3))
        street11 = StreetSegment(Pvector(5,-8),Pvector(4,-3))
        street12 = StreetSegment(Pvector(5,-8), Pvector(12,-1))
        self.street_segment_list.append(street1)
        self.street_segment_list.append(street2)
        self.street_segment_list.append(street3)
        self.street_segment_list.append(street4)
        self.street_segment_list.append(street5)
        self.street_segment_list.append(street6)
        self.street_segment_list.append(street7)
        self.street_segment_list.append(street8)
        self.street_segment_list.append(street9)
        self.street_segment_list.append(street10)
        self.street_segment_list.append(street11)
        self.street_segment_list.append(street12)

    def get_street_segment_list(self):
        return self.street_segment_list
