from pvector import *
print('Pvector Test')

a = Pvector(1,2)
b = Pvector(2,4)
alpha = 4
print('a = ',a.x, a.y)
print('b = ',b.x, b.y)

c = a.add(b)
print(c.x, c.y)
d = a.substract(b)
print(d.x, d.y)
e = a.multiplyScalar(alpha)
print(e.x, e.y)
f = a.divideScalar(alpha)
print(f.x,f.y)

f2 = a.divideScalar(0)
print(f.x, f.y)

h = a.magnitudeSquared();
print(h)
input('Press enter to close')
