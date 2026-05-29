import MeatEngine.Math.vector as vector
import triangle
import Image
import math
import intersect
import light

verts=[vector.Vec3f(-1.0, -1.0, -1.0),
       vector.Vec3f(-1.0, -1.0,  1.0),
       vector.Vec3f(-1.0,  1.0, -1.0),
       vector.Vec3f(-1.0,  1.0,  1.0),
       vector.Vec3f( 1.0, -1.0, -1.0),
       vector.Vec3f( 1.0, -1.0,  1.0),
       vector.Vec3f( 1.0,  1.0, -1.0),
       vector.Vec3f( 1.0,  1.0,  1.0),

       vector.Vec3f(-1.0, 3.0, -1.0),
       vector.Vec3f(-1.0, 5.0, -1.0),
       vector.Vec3f(0.73, 4.0, -1.0),
       vector.Vec3f(-.42, 4.0, 0.63),

       vector.Vec3f(-5.5, -5.5, -1.0),
       vector.Vec3f(-5.5,  5.5, -1.0),
       vector.Vec3f( 5.5, -5.5, -1.0),
       vector.Vec3f( 5.5,  5.5, -1.0),
       ]

tris=[(2, 0, 1),
      (1, 3, 2),
      (6, 4, 0),
      (0, 2, 6),
      (6, 2, 3),
      (3, 7, 6),
      (5, 4, 6),
      (6, 7, 5),
      (1, 0, 4),
      (4, 5, 1),
      (1, 5, 7),
      (7, 3, 1),

      (8, 9, 10),
      (8, 10, 11),
      (9, 11, 10),
      (8, 11, 9),

      (12, 14, 13),
      (14, 15, 13)
      ]

colors=[(240, 0, 0),
        (240, 0, 0),
        (0, 240, 0),
        (0, 240, 0),
        (0, 0, 240),
        (0, 0, 240),
        (180, 180, 0),
        (180, 180, 0),
        (180, 0, 180),
        (180, 0, 180),
        (0, 180, 180),
        (0, 180, 180),

        (0, 0, 0),
        (200, 200, 200),
        (200, 200, 200),
        (250, 250, 250),

        (220, 220, 220),
        (220, 220, 220)]


TOT_FRAMES=150

WIDTH=400
HEIGHT=200

FOV=math.radians(50)
NEAR=0.5

LIGHT_DIR=vector.Vec3f(-0.5,-0.5, -1.0).norm()
dirLight=light.DirectionalLight(LIGHT_DIR,
                                (1.0, 1.0, 1.0))

AMBIENT=0.25
LIGHT_VAL=0.75

def trace(base, frameNum):
    print "Frame:",frameNum
    radius=9.0
    x=radius*math.cos(2*math.pi*frameNum/TOT_FRAMES)
    y=radius*math.sin(2*math.pi*frameNum/TOT_FRAMES)
    z=3.0
    
    eye=vector.Vec3f(x, y, z)
    at=vector.Vec3f(0.0, 0.0, 0.0)
    worldUp=vector.Vec3f(0.0, 0.0, 1.0)

    aspect=float(WIDTH)/HEIGHT

    halfFOVangle=FOV/2.0
    step=math.tan(halfFOVangle)*NEAR/(WIDTH/2.0)

    eyeForward=at.sub(eye).norm().mul(NEAR)
    eyeRight=eyeForward.cross(worldUp).norm().mul(step)
    eyeUp=eyeRight.cross(eyeForward).norm().mul(step)

    im=Image.new("RGB", (WIDTH,HEIGHT))

    for x in range(WIDTH):
        xVec=eyeRight.mul(x-WIDTH/2)
        
        for y in range(HEIGHT):
            yVec=eyeUp.mul(y-HEIGHT/2)
    
            dir=eyeForward.add(xVec.add(yVec))
    
            closestDepth=None
            bestColor=(200,200,200)
            
            for triIndex, tverts in enumerate(tris):
                c=colors[triIndex]
    
                triVerts=[verts[i] for i in tverts]
    
                ix=triangle.intersectRayTriangle(eye,
                                                 dir,
                                                 triVerts[0],
                                                 triVerts[1],
                                                 triVerts[2],
                                                 True)
    
                if ix:
                    t=ix.dist
                    u,v=ix.uv

                    iNorm=ix.normal.norm()

                    lightDot=-iNorm.dot(LIGHT_DIR)

                    if lightDot>0:
                        # now raycast to see if we're occluded
                        for lightTriIndex,lightTVerts in enumerate(tris):
                            if lightTriIndex==triIndex:
                                continue
                            lightTriVerts=[verts[i] for i in lightTVerts]
                            lx=triangle.intersectRayTriangle(ix.pos,
                                                             LIGHT_DIR.mul(-1.0),
                                                             lightTriVerts[0],
                                                             lightTriVerts[1],
                                                             lightTriVerts[2],
                                                             True)
                            if lx and lx.dist>0:
                                lightDot=0
                                break

                    if lightDot<0:
                        lightDot=0

                    totalLight=AMBIENT+LIGHT_VAL*lightDot

                    if (closestDepth is None or
                        (t>0 and t<closestDepth)):
                        closestDepth=t
                        cr,cg,cb=c

                        #bestColor=(cr,
                        #           120+int(128*u),
                        #           120+int(128*v))
                        bestColor=c


                        bestColor=(cr*totalLight,
                                   cg*totalLight,
                                   cb*totalLight)
    
            im.putpixel((x,HEIGHT-y-1), bestColor)
            
    im.save("%s%04d.png"%(base,frameNum))
        

if __name__=="__main__":
    for i in range(TOT_FRAMES):
        trace("light", i)
       


