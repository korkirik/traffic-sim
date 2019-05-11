class JunctionPoint(Pvector):
    def __init__(self, x, y, i):
    self.x = float(x)
    self.y = float(y)
    self.i = int(i)

    #If this junction point can take you to next junction, it's accessible.
    # Otherwise, it's not (e.g. at the corner)
    accessible = true
    # A street has only two ends, one is to drive in,
    #the other is to drive out
    inOrOut = true
    #It's used to record the relative position of the
    # junction points at the junction
    index = i

    #Return a junction point object
def get():
    return self #Lets try this -K
