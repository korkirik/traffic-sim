from pvector import *
print('Pvector Test')

a = Pvector(1,2)
b = Pvector(2,4)
alpha = 2
print('a = ',a.x, a.y)
print('b = ',b.x, b.y)

#c = a.add(b)
#print(c.x, c.y)
#d = a.substract(b)
#print(d.x, d.y)

#e = a.multiplyByScalar(alpha)
#print(e.x, e.y)
#f = a.divideByScalar(alpha)
#print(f.x,f.y)

#f2 = a.divideByScalar(0)
#print(f2.x, f2.y)

#h = a.magnitudeSquared()
#i = a.magnitude()
#print(h)
#print(i)
#print(a.x, a.y)
#a.normalize()
q = a.get()
a.setMagnitude(5)
q.limitMagnitude(4)
print(q.x, q.y)
print(q.magnitude())

input('Press enter to close')
