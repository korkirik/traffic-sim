'''
/*****************************************************************
 * Project:     Traffic Simulation through Agent-based Modelling
 *
 * Lecture:     System & Self-Organization
 *              Sommer Semester 2017, Hochschule Rhein-Waal
 *              &&
 *              Sommer Semester 2019, Hochschule Rhein-Waal
 *
 * Objective:   This project demonstrates the emergent behavior
 *              that takes place among a group of drivers travelling
 *              in a pre-defined map. The traffic flow depends not
 *              only on the number of agents in the city, but also
 *              the interaction between them. The behavior of one
 *              driver is influenced by other drivers on the street
 *              as well as other factors like traffic jam. An overall
 *              emergent effect is thereby generated and is observable.
 *
 * Author:      Yu-Jeng Kuo, Arindam Mahanta, Anoshan Indreswaran
 * Ported into Python by: Yusuf Ismail, Kirill Korolev, Leen Nijim
 *
 * Last update: 24.04.2019
 ******************************************************************/
'''
from junction import *
from path import*
from array import *

from bokeh.plotting import figure, output_file, show
output_file("test.html")

q = Junction(0,0)
q.whoAmI()

path = Path()
p = figure()
length = len(path.mainJunctions)
xl = list()
yl = list()
a = list()
for jun in range(0,length,1):
    xl = path.mainJunctions[jun].junLocation.x
    yl = path.mainJunctions[jun].junLocation.y
    print(xl,yl)
    a = (xl,yl)
#p = figure(plot_width=400, plot_height=400)
#p.line(a, line_width=2)

p.image(image = [a], x=0 , y=0, dw =2, dh =2, palette="Spectral11")
show(p)


show(p)
