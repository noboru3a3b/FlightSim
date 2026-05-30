"""Voronoi/Delaunay Subdivision code

transcribed from Graphics Gems IV"""


import quadedge
import predicates

EPSILON=0.01

class Subdivision:
    def __init__(self, a, b, c):
        ea = quadedge.makeEdge()
        ea.endPoints(a,b)

        eb = quadedge.makeEdge()
        quadedge.splice(ea.sym, eb)
        eb.endPoints(b,c)

        ec = quadedge.makeEdge()
        quadedge.splice(eb.sym, ec)
        ec.endPoints(c,a)

        quadedge.splice(ec.sym, ea)
        self.startingEdge = ea


    def debugPrint(self):
        e=self.dumpEdges()

        print "subdivision edges"
        print "="*40
        for edge in e:
            print edge
        print "="*40

        for edge in e:
            print edge
            print "oNext",edge.oNext()
            print "oPrev",edge.oPrev()
            print "dNext",edge.dNext()
            print "dPrev",edge.dPrev()
            print "lNext",edge.lNext()
            print "lPrev",edge.lPrev()
            print "rNext",edge.rNext()
            print "rPrev",edge.rPrev()
            print "-"*20
    
        

    def insertSite(self, x):
        e = self.locate(x)

        if (x.samePoint(e.org(), EPSILON) or
            x.samePoint(e.dest(), EPSILON)):
            # already there
            return
        elif predicates.onEdge(x,e):
            e = e.oNext()
            quadedge.deleteEdge(e.oNext())


        base = quadedge.makeEdge()

        base.endPoints(e.org(), x)
        quadedge.splice(base, e)
        self.startingEdge = base

        while 1:
            base = connect(e, base.sym)
            e = base.oPrev()

            if e.lNext() is self.startingEdge:
                break

        while 1:
            t = e.oPrev()
            if (predicates.rightOf(t.dest(), e) and
                predicates.inCircle(e.org(), t.dest(), e.dest(), x)):
                swap(e)
                e = e.oPrev()
            elif e.oNext() is self.startingEdge:
                return
            else:
                e = e.oNext().lPrev()

    def draw(self):
        print
        for d in self.dumpEdges():
            print d

    def dumpEdges(self):
        drawnEdges=[]
        openEdges=[self.startingEdge]
        self.startingEdge.tag=1

        while openEdges:
            e=openEdges.pop()
            drawnEdges.append(e)
            neighbors=[e.sym,
                       e.oNext(),
                       e.oPrev(),
                       e.dNext(),
                       e.dPrev()]
            for n in neighbors:
                if not n.tag:
                    n.tag=1
                    openEdges.append(n)

        for d in drawnEdges:
            d.tag=0
        return drawnEdges

    def locate(self, x):
        """returns an edge e, st either x is on e or e is an edge of a
        triangle containing x. The search starts from the startingEdge
        and proceeds in the general direction of x. Based on the
        pseudocode in Guibas and Stolfi (1985, p. 121)."""


        e=self.startingEdge

        while 1:
            if (x.samePoint(e.org(), EPSILON) or
                x.samePoint(e.dest(), EPSILON)):
                return e
            elif predicates.rightOf(x,e):
                e = e.sym
            elif not predicates.rightOf(x, e.oNext()):
                e = e.oNext()
            elif not predicates.rightOf(x, e.dPrev()):
                e = e.dPrev()
            else:
                return e
            
        


def connect(a, b):
    e=quadedge.makeEdge()
    quadedge.splice(e, a.lNext())
    quadedge.splice(e.sym, b)
    e.endPoints(a.dest(), b.org())
    return e


def swap(e):
    a = e.oPrev()
    b = e.sym.oPrev()
    quadedge.splice(e, a)
    quadedge.splice(e.sym, b)
    quadedge.splice(e, a.lNext())
    quadedge.splice(e.sym, b.lNext())
    e.endPoints(a.dest(), b.dest())


