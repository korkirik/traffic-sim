import random
from parser_osm import Parser
from streetsegment import *

class PseudoParser_Testground(Parser):
    def __init__(self):
            self.streetSegmentList = list()
            self.getData()

    def getData(self):
        street1 = StreetSegment(Pvector(0,0), Pvector(5,2))
        street2 = StreetSegment(Pvector(5,2), Pvector(12,-1))
        street3 = StreetSegment(Pvector(12,-1), Pvector(16,2))
        street4 = StreetSegment(Pvector(12,-1), Pvector(15,-5))

        self.streetSegmentList.append(street1)
        self.streetSegmentList.append(street2)
        self.streetSegmentList.append(street3)
        self.streetSegmentList.append(street4)

    def getStreetSegmentList(self):
        return self.streetSegmentList
