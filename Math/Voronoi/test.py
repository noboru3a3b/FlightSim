#
# mapmaker.py
#
# What if we made a Poisson Disc Distribution of positions on the
# board, and then proceeded to triangulate those positions (somehow)
# and then drew the dual graph of the resultant network? Would that be
# an interesting gameboard?

import Image, ImageDraw
import random
import math

import subdivision
import sys
sys.path.append(r"e:\dev")
from MeatEngine.Math.vector import Vec2f

EPSILON=0.001
imX=2400
imY=3000

greenGrass=(128,255,128)
greyGreen=(100,240,100)

backgroundColor=(255,255,255)
adjacencyColor=(180,240,240)


def findCircumCenter(p1, p2, p3):
    """
    From a post by Dave Watson:
    
    This approach uses Cramer's Rule to find the intersection of two
    perpendicular bisectors of triangle edges

    
    p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) 
    -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) 
    / D

    p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0)
    -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0))
    / D

    where D = (a_0 - c_0) * (b_1 - c_1) - (b_0 - c_0) * (a_1 - c_1)

    The _squared_ circumradius is then:

    r^2 = (c_0 - p_0)^2 + (c_1 - p_1)^2
    """

    d = (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    if abs(d) < EPSILON:
        return ((p1.x+p2.x+p3.x)/3,
                (p1.y+p2.y+p3.y)/3)

    x = (((p1.x - p3.x) * (p1.x + p3.x) + (p1.y - p3.y) * (p1.y + p3.y)) / 2 *
         (p2.y - p3.y) -
         ((p2.x - p3.x) * (p2.x + p3.x) + (p2.y - p3.y) * (p2.y + p3.y)) / 2 *
         (p1.y - p3.y)) / d

    y = (((p2.x - p3.x) * (p2.x + p3.x) + (p2.y - p3.y) * (p2.y + p3.y)) / 2 * (p1.x - p3.x)
         -  ((p1.x - p3.x) * (p1.x + p3.x) + (p1.y - p3.y) * (p1.y + p3.y)) / 2 * (p2.x - p3.x))/ d
    
    return x,y

    
        
    
def pointIsValid(p, rSqr):
    for p1 in points:
        dx=p1[0]-p[0]
        dy=p1[1]-p[1]

        distSqr=dx*dx+dy*dy
        if distSqr<rSqr:
            return False
    return True
        
    
if __name__=="__main__":
    im=Image.new("RGB",(imX,imY),backgroundColor)
    draw=ImageDraw.ImageDraw(im)

    points=[]
    
    radius=60
    numPts=15000
    
    
    p1=Vec2f(-100.0,-100.0)
    p2=Vec2f(3.0*imX,0.0)
    p3=Vec2f(0.0,3.0*imY)
    
    s=subdivision.Subdivision(p1,p2,p3)

    for i in range(numPts):
        print i
        x=float(random.randrange(imX))
        y=float(random.randrange(imY))
    
        rSqr=radius*radius
        
        p=(x,y)
        if pointIsValid(p,rSqr):
            points.append(p)
            s.insertSite(Vec2f(x,y))
            im.putpixel(p,(0,0,0))

    
    e=s.dumpEdges()
    for edge in e:
        o=edge.org()
        d=edge.dest()
        q1=edge.lNext().dest()
        q2=edge.sym.lNext().dest()
    
        x1,y1=findCircumCenter(o,d,q1)
        x2,y2=findCircumCenter(o,d,q2)
        
        draw.line((o.x, o.y, d.x, d.y), adjacencyColor)
        draw.line((x1, y1, x2, y2), (0,0,0))
    
    del draw
    
    im.save("map.jpg")
    
