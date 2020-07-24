import math
from pvector import Pvector

#converts coordinate point into Web Mercator Coordinates
class Converter:

    def __init__(self):
        self.radius = 6378137

    def convert(self, long, lat):
        x = long * (math.pi/180) * self.radius
        y = math.log( math.tan( lat * (math.pi/360) + math.pi/4) ) * self.radius
        #print('{} {}'.format(x,y))
        return (x,y)

    def convert_point(self, long, lat):
        x,y = self.convert(long,lat)
        return Pvector(x,y)


    def convert_longitude_range(self, long1, long2):
        x1 = long1 * (math.pi/180) * self.radius
        x2 = long2 * (math.pi/180) * self.radius
        return (x1,x2)

    def convert_latitude_range(self, lat1, lat2):
        y1 = math.log( math.tan( lat1 * (math.pi/360) + math.pi/4) ) * self.radius
        y2 = math.log( math.tan( lat2 * (math.pi/360) + math.pi/4) ) * self.radius
        return (y1,y2)

    def convert_point_to_geocoordinates(self, x, y):
        long = x / ((math.pi/180) * self.radius)
        lat = (math.atan( math.exp(y / (self.radius))) - math.pi/4 ) * 360/math.pi
        return (long, lat)
