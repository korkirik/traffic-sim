import random
from parser_osm import Parser
from streetsegment import *

class PseudoParser(Parser):
    def __init__(self):
            self.streetSegmentList = list()

    def parseFile(self):
        street1 = StreetSegment(Pvector(0,0), Pvector(5,2))
        street2 = StreetSegment(Pvector(2,5), Pvector(5,2))
        street3 = StreetSegment(Pvector(5,2), Pvector(11,1))
        street4 = StreetSegment(Pvector(11,1), Pvector(14,4))
        street5 = StreetSegment(Pvector(11,1), Pvector(10,-5))
        street6 = StreetSegment(Pvector(2,5), Pvector(random.randrange(-10, 10, 1), random.randrange(5, 30, 1)))
        street7 = StreetSegment(Pvector(0,0), Pvector(random.randrange(-20, 0, 1), random.randrange(-20, 20, 1)))
        street8 = StreetSegment(Pvector(14,4), Pvector(random.randrange(14, 30, 1), random.randrange(-30, 30, 1)))
        street9 = StreetSegment(Pvector(10,-5), Pvector(random.randrange(-30, 30, 1), random.randrange(-30, -5, 1)))
        street10 = StreetSegment(Pvector(0,0),Pvector(10,-5))
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
