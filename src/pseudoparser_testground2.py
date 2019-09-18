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
        street5 = StreetSegment(Pvector(15,-5), Pvector(12,-10))
        street6 = StreetSegment(Pvector(12,-10), Pvector(5,-8))
        street7 = StreetSegment(Pvector(1,-6), Pvector(5,-8))
        street8 = StreetSegment(Pvector(0,0), Pvector(1,-6))
        street9 = StreetSegment(Pvector(5,2), Pvector(4,-3))
        street10 = StreetSegment(Pvector(0,0),Pvector(4,-3))
        street11 = StreetSegment(Pvector(5,-8),Pvector(4,-3))
        street12 = StreetSegment(Pvector(5,-8), Pvector(12,-1))
        self.streetSegmentList.append(street1)
        self.streetSegmentList.append(street2)
        self.streetSegmentList.append(street3)
        self.streetSegmentList.append(street4)
        self.streetSegmentList.append(street5)
        self.streetSegmentList.append(street6)
        self.streetSegmentList.append(street7)
        self.streetSegmentList.append(street8)
        self.streetSegmentList.append(street9)
        self.streetSegmentList.append(street10)
        self.streetSegmentList.append(street11)
        self.streetSegmentList.append(street12)
    def getStreetSegmentList(self):
        return self.streetSegmentList
