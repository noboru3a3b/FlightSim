""" Voronoi/Delaunay predicates

transcribed from Graphics Gems IV"""

import quadedge

EPSILON=0.01

def triArea(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def inCircle(a, b, c, d):
    return ((a.x*a.x + a.y*a.y) * triArea(b, c, d) -
            (b.x*b.x + b.y*b.y) * triArea(a, c, d) +
            (c.x*c.x + c.y*c.y) * triArea(a, b, d) -
            (d.x*d.x + d.y*d.y) * triArea(a, b, c)) > 0


def ccw(a, b, c):
    ta=triArea(a, b, c)
    return ta>0

def rightOf(x, e):
    return ccw(x, e.dest(), e.org())

def leftOf(x, e):
    return ccw(x, e.org(), e.dest())

def onEdge(x, e):
    t1 = x.sub(e.org()).mag()
    t2 = x.sub(e.dest()).mag()
    if (t1 < EPSILON) or (t2 < EPSILON):
        return True

    t3 = e.org().sub(e.dest()).norm()
    if (t1 > t3) or (t2>t3):
        return False

    #line = vect2d.Line(e.org(), e.dest())
    #return abs(line.eval(x))<EPSILON

    return False


    

