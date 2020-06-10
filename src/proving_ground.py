import random
from parser_streets import Parser
from streetsegment import *

class ProvingGround(Parser):
    def __init__(self):
            self.street_segment_list = list()
            self.get_data()

    def get_data(self):
        street1 = StreetSegment(Pvector(1,1), Pvector(6,1))
        street2 = StreetSegment(Pvector(6,6), Pvector(6,1))
        street3 = StreetSegment(Pvector(6,1), Pvector(11,1))
        self.street_segment_list.append(street1)
        self.street_segment_list.append(street2)
        self.street_segment_list.append(street3)

    def get_street_segment_list(self):
        return self.street_segment_list
