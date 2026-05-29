""" Quadedge data structure, after Guibas and Stolfi

Transcribed from Graphics Gems IV

sym: "symmetric" of edge, the edge that points in the opposite
direction (when viewed from the same orientation of the manifold).

vertices are also represented as "edges", because a quadEdge object
has four edge sub-structures to represent an edge - two substructures
for there and back, and the vertices at the ends form a circular
linked list.


"""



class QuadEdge:
    def __init__(self):
        self.edges=(Edge(), Edge(), Edge(), Edge())
        e=self.edges
        e[0].num=0
        e[1].num=1
        e[2].num=2
        e[3].num=3
        e[0].next=e[0]
        e[1].next=e[3]
        e[2].next=e[2]
        e[3].next=e[1]
        
        e[0].sym=e[2]
        e[1].sym=e[3]
        e[2].sym=e[0]
        e[3].sym=e[1]
        
        e[0].rot=e[1]
        e[1].rot=e[2]
        e[2].rot=e[3]
        e[3].rot=e[0]

        e[0].invRot=e[3]
        e[1].invRot=e[0]
        e[2].invRot=e[1]
        e[3].invRot=e[2]
        
class Edge:
    def __init__(self):
        self.num=0
        self.next=None
        self.data=None
        self.sym=None
        self.tag=0

    def oNext(self):
        """next edge ccw with same origin"""
        return self.next

    def oPrev(self):
        """prev edge ccw with same origin"""
        return self.rot.oNext().rot

    def dNext(self):
        """next edge ccw with the same destination"""
        return self.sym.oNext().sym

    def dPrev(self):
        """prev edge with the same destination"""
        return self.invRot.oNext().invRot

    def lNext(self):
        """next edge around left face of current edge"""
        return self.invRot.oNext().rot

    def lPrev(self):
        """prev edge around left face of current edge"""
        return self.oNext().sym

    def rNext(self):
        """next edge around right face of current edge"""
        return self.rot.oNext().invRot

    def rPrev(self):
        """prev edge around right face of current edge"""
        return self.sym.oNext()

    def org(self):
        """origin of edge"""
        return self.data

    def dest(self):
        """destination of edge"""
        return self.sym.data

    def endPoints(self, org, dst):
        """set endpoints"""
        self.data=org
        self.sym.data=dst

    def __str__(self):
        return str(self.org())+" -> "+str(self.dest())

def makeEdge():
    q1 = QuadEdge()
    return q1.edges[0]

def splice(a, b):
    alpha = a.oNext().rot
    beta  = b.oNext().rot
    t1 = b.oNext()
    t2 = a.oNext()
    t3 = beta.oNext()
    t4 = alpha.oNext()
    a.next=t1
    b.next=t2
    alpha.next=t3
    beta.next=t4

def deleteEdge(e):
    splice(e, e.oPrev())
    splice(e.sym,e.sym.oPrev())


