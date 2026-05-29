"""Pastel Sombrero map generation tool

Want to support a variety of terrain types

 - seussian pastel mesas
 - moon craters
 - rolling hills
 - islands

The basic pattern will be to create a vertex array and an indexed tristrip.
"""

import math
import MeatEngine
from MeatEngine.Math.vector import Vec3f

import model

colors=[(248,161,206), #pink
        (183,255,149), #green
        (73,252,230),  #turquoise
        (255,191,85),  #orange
        (189,188,246), #lavender
        (252, 255, 115)] #yellow

colors=[[c/255.0 for c in clr] for clr in colors]

def makeSeussMesa(vCenter):
    height=50.0

    numNeckRings=8
    neckHeight=5.0
    neckBottomRadius=17.0
    neckTopRadius=5.0
    numShoulderRings=10
    shoulderBottomRadius=65.0

    baseSpace=5.0

    ringVerts={}

    # store the verts in the dictionary, counting up from the shoulder.
    
    for shoulderIndex in range(numShoulderRings+1):
        frac=float(shoulderIndex)/numShoulderRings
        thisRadius=(1.0-frac)*(shoulderBottomRadius-neckBottomRadius)+neckBottomRadius
        thisCircumference=2*math.pi*thisRadius
        #numVerts=int(thisCircumference/baseSpace)
        numVerts=36
        thisAlt=frac*(neckHeight)

        vertList=[]
        for vertIndex in range(numVerts):
            vertFrac=float(vertIndex)/numVerts
            radians=vertFrac*2*math.pi
            x=math.cos(radians)
            y=math.sin(radians)

            v=Vec3f(x*thisRadius,
                    y*thisRadius,
                    thisAlt).add(vCenter)
            vertList.append(v)
        ringVerts[shoulderIndex]=vertList

    for neckIndex in range(1,numNeckRings+1):
        frac=float(neckIndex)/numNeckRings
        thisRadius=(1.0-frac)*(neckBottomRadius-neckTopRadius)+neckTopRadius
        thisCircumference=2*math.pi*thisRadius
        #numVerts=int(thisCircumference/baseSpace)
        numVerts=36
        thisAlt=frac*(height-neckHeight)+neckHeight

        vertList=[]
        for vertIndex in range(numVerts):
            vertFrac=float(vertIndex)/numVerts
            radians=vertFrac*2*math.pi
            x=math.cos(radians)
            y=math.sin(radians)

            v=Vec3f(x*thisRadius,
                    y*thisRadius,
                    thisAlt).add(vCenter)
            vertList.append(v)
        ringVerts[neckIndex+numShoulderRings]=vertList


    m=model.Model()

    vertexTable={}

    ringIndices = sorted(ringVerts.keys())
    
    for ringNum in ringIndices:
        numVertsInRing=len(ringVerts[ringNum])
        startVertIndex=len(m.verts)
        for i,v in enumerate(ringVerts[ringNum]):
            index=len(m.verts)
            m.verts.append(v)
            vertexTable[(ringNum,i)]=index
        for i in range(numVertsInRing):
            m.lines.append((startVertIndex+i,
                            startVertIndex+((i+1)%numVertsInRing)))


    for ringNum in ringIndices:
        nextRingNum=ringNum+1
        if nextRingNum not in ringIndices:
            continue
        numVertsInRing=len(ringVerts[ringNum])
        for vertIndex in range(numVertsInRing):
            nextVertIndex=(vertIndex+1)%numVertsInRing

            thisVert=ringVerts[ringNum][vertIndex]

            bestDist=3000.0
            bestIndex=-1

            for nextRingVertIndex in range(len(ringVerts[nextRingNum])):
                nextRingVert=ringVerts[nextRingNum][nextRingVertIndex]

                dsqr=nextRingVert.sub(thisVert).magSqr()

                if dsqr<bestDist:
                    bestDist=dsqr
                    bestIndex=nextRingVertIndex
                    
            assert bestIndex != -1

            t={}

            #t['color']=(ringNum%3/2.0,
            #            ringNum%4/3.0,
            #            ringNum%6/5.0)
            
            t['color']=colors[ringNum%len(colors)]
            
            t['indices']=(vertexTable[(ringNum,vertIndex)],
                          vertexTable[(ringNum,nextVertIndex)],
                          vertexTable[(nextRingNum,bestIndex)])

            m.tris.append(t)

    for ringNum in ringIndices:
        prevRingNum=ringNum-1
        if prevRingNum not in ringIndices:
            continue
        numVertsInRing=len(ringVerts[ringNum])
        for vertIndex in range(numVertsInRing):
            nextVertIndex=(vertIndex+numVertsInRing-1)%numVertsInRing

            thisVert=ringVerts[ringNum][vertIndex]

            bestDist=3000.0
            bestIndex=-1

            for prevRingVertIndex in range(len(ringVerts[prevRingNum])):
                prevRingVert=ringVerts[prevRingNum][prevRingVertIndex]

                dsqr=prevRingVert.sub(thisVert).magSqr()

                if dsqr<bestDist:
                    bestDist=dsqr
                    bestIndex=prevRingVertIndex
                    
            assert bestIndex != -1

            t={}

            #t['color']=(prevRingNum%3/2.0,
            #            prevRingNum%4/3.0,
            #            prevRingNum%6/5.0)

            t['color']=colors[prevRingNum%len(colors)]
            
            t['indices']=(vertexTable[(ringNum,vertIndex)],
                          vertexTable[(ringNum,nextVertIndex)],
                          vertexTable[(prevRingNum,bestIndex)])

            m.tris.append(t)
                           
            

    
                           
            
    return m

        
        
        
    
    
if __name__=="__main__":
    center = Vec3f(0.0, 0.0, 0.0)

    mesa = makeSeussMesa(center)

    # Show a brief summary when run as a script
    try:
        print("vertex count:", len(mesa.verts))
        for i, v in enumerate(mesa.verts[:10]):
            print(i, v)
    except Exception:
        print("Created model, unable to display vertices")
        
