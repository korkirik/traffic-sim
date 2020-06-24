from bokeh.plotting import figure, output_file, show
from bokeh.models import MapOptions
from bokeh.tile_providers import OSM, get_provider
import math

#converts coordinate point into Web Mercator Coordinates
class Converter:
    def __init__(self):
        self.radius = 6378137

    def convert_point(self, long, lat):

        x = long * (math.pi/180) * self.radius
        y = math.log( math.tan( lat * (math.pi/360) + math.pi/4) ) * self.radius
        #print('{} {}'.format(x,y))
        return (x,y)

    def convert_longitude_range(self, long1, long2):
        x1 = long1 * (math.pi/180) * self.radius
        x2 = long2 * (math.pi/180) * self.radius
        return (x1,x2)

    def convert_latitude_range(self, lat1, lat2):
        y1 = math.log( math.tan( lat1 * (math.pi/360) + math.pi/4) ) * self.radius
        y2 = math.log( math.tan( lat2 * (math.pi/360) + math.pi/4) ) * self.radius
        return (y1,y2)

output_file("tile.html")
c = Converter()

tile_provider = get_provider(OSM)

p = figure(x_range=c.convert_longitude_range(6.06, 6.20), y_range=c.convert_latitude_range(51.74, 51.82),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

show(p)
