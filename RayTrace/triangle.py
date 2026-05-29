import MeatEngine.Math.vector
import intersect

EPSILON=0.000001

"""
from "Fast, Minimum Storage Ray/Triangle Intersection" by Moller and
Trumbore
"""


def intersectRayTriangle(orig, dir,
                         v0, v1, v2,
                         cullBackface=False):
    """
    intersectTriangle takes 5 points (origin, direction, and three
    vertices) and returns a distance and a u,v
    """

    edge1=v1.sub(v0)
    edge2=v2.sub(v0)

    pVec = dir.cross(edge2)
    det = edge1.dot(pVec)

    if cullBackface:
        if det<EPSILON:
            # backfacing, return None
            return None

        tVec=orig.sub(v0)
        u=tVec.dot(pVec)
        if (u < 0 or u > det):
            return None

        qVec=tVec.cross(edge1)

        v=dir.dot(qVec)
        if (v < 0 or v > det):
            return None

        t=edge2.dot(qVec)
        invDet=1.0/det

        t *= invDet
        u *= invDet
        v *= invDet
    else:
        #not culling

        if (det > -EPSILON and det < EPSILON):
            # edge-on
            return None

        invDet= 1.0/det
        tVec=orig.sub(v0)

        u=tVec.dot(pVec)*invDet
        if (u<0.0 or u>1.0):
            return None

        qVec=tVec.cross(edge1)

        v=dir.dot(qVec)*invDet

        if (v<0.0 or v>1.0):
            return None

        t=edge2.dot(qVec)*invDet

    if u+v>1:
        return None

    pos=v0.add(edge1.mul(u).add(edge2.mul(v)))
    
    return intersect.Intersection(t,
                                  pos,
                                  (u,v),
                                  edge1.cross(edge2))



