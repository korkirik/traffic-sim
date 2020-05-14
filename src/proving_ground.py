import random
from parser_streets import Parser
from streetsegment import *

class ProvingGround(Parser):
    def __init__(self):
            self.street_segment_list = list()
            self.get_data()

    def get_data(self):
        street1 = StreetSegment(Pvector(4,-2), Pvector(10,0))
        street2 = StreetSegment(Pvector(10,0), Pvector(14,-6))
        #street3 = StreetSegment(Pvector(17,2), Pvector(20,2))
        self.street_segment_list.append(street1)
        self.street_segment_list.append(street2)
        #self.street_segment_list.append(street3)

    def get_street_segment_list(self):
        return self.street_segment_list
