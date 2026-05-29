import math
import os
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
try:
    from OpenGL.WGL.EXT.swap_control import *
    swap_control=1
except:
    swap_control=0

from OpenGL.GL.ARB.multitexture import *

import pygame, pygame.image
from pygame.locals import *

from MeatEngine.Math.vector import Vec3f
import makeMap
import plane
import target

dots=[]

gMesas=[]
gTargets=[]

gPosList=[Vec3f(30.0, 70.0, 20.0),
          Vec3f(100.0, 10.0, 80.0),
          Vec3f(-1.7, -88.0, 57.0),
          Vec3f(87.0, -58.0, 19.0),
          Vec3f(-67.0, 31.0, 34.0),
          Vec3f(40.0, -50.0, 56.0),
          Vec3f(28.0, -51.0, 50.0),
          Vec3f(77.0, -56.0, 70.0),
          Vec3f(41.0, 44.0, 10.0),
          Vec3f(-58.0, -49.0, 26.0)]
          

gPlane=None
gCameraPos=Vec3f(100.0, 100.0, 60.0)

gTime=0.0

SCREEN_SIZE=(800,600)

def resize(width, height):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0*width/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    #glEnable(GL_TEXTURE_2D)
    #glShadeModel(GL_SMOOTH)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glClearDepth(100.0)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glShadeModel (GL_FLAT)
    glLineWidth(1.5)
    glPointSize(2.0)

    glInitMultitextureARB()    


def drawModel(m):

    glBegin(GL_TRIANGLES)
    for t in m.tris:
        glColor3f(*t['color'])
    
        for vi in t['indices']:
            v=m.verts[vi]
            glVertex3f(v.x, v.y, v.z)
    glEnd()
        
    
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for i1, i2 in m.lines:
        v1=m.verts[i1]
        v2=m.verts[i2]

        for v in (v1,v2):
            glVertex3f(v.x, v.y, v.z)
    glEnd()


def drawRadar():
    radarSize=80
    radarX=700.0
    radarY=500.0
    numSteps=32

    glColor3f(0.5, 1.0, 0.5)
    glBegin(GL_LINE_LOOP)
    for i in range(numSteps):
        f=float(i)/numSteps
        radians=f*2*math.pi

        x=math.cos(radians)
        y=math.sin(radians)
        glVertex2f(x*radarSize+radarX,
                   y*radarSize+radarY)
    glEnd()

    for t in gTargets:
        tx,ty,tz=t.pos.x,t.pos.y,t.pos.z
        dx=tx-gPlane.pos.x
        dy=ty-gPlane.pos.y
        dz=tz-gPlane.pos.z

        if dz>t.size:
            glColor3f(1.0, 0.0, 0.0)
        elif dz<-t.size:
            glColor3f(0.0, 0.0, 1.0)
        else:
            glColor3f(0.0, 1.0, 0.0)

        h=math.atan2(dy,dx)
        planeHeadingRadians=math.radians(gPlane.heading)
        relHeading=h-planeHeadingRadians+math.radians(90.0)

        x=math.cos(relHeading)
        y=math.sin(relHeading)

        glBegin(GL_LINES)
        glVertex2f(radarX,
                   radarY)
        glVertex2f(x*radarSize+radarX,
                   y*radarSize+radarY)
        glEnd()
        
                   


def drawUI():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    drawRadar()
    

    

def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 4.0/3.0, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    planePos=gPlane.pos
    px,py,pz=planePos.x, planePos.y, planePos.z
    gluLookAt( gCameraPos.x, gCameraPos.y, gCameraPos.z,
                 px,    py,      pz,
                0.0,   0.0,     1.0)

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    for tm, pos in dots:
        glVertex3f(pos.x, pos.y, pos.z)
    glEnd()        
        

    for m in gMesas:
        drawModel(m)

    for t in gTargets:
        t.draw(gTime)

    gPlane.draw()

    drawUI()


def handleEvent(e):
    if e.type == KEYDOWN:
        if e.key==K_ESCAPE:
            sys.exit()
    
    
def updateCamera(dt):
    global gCameraPos

    headingRadians=math.radians(gPlane.heading)
    lagVector=Vec3f(math.cos(headingRadians),
                    math.sin(headingRadians),
                    -0.5).norm().mul(-50.0)
    idealPos=gPlane.pos.add(lagVector)
    
    #print "camPos",gCameraPos
    #print "planePos",gPlane.pos
    separation=idealPos.sub(gCameraPos)

    sepMag=separation.mag()
    #print "sep:",sepMag
    
    #let's say we want the desired separation to be the velocity

    desiredLen=50.0

    deltaLen=sepMag-desiredLen

    #close the distance in two seconds, say
    timeToClose=0.1

    closeSpeed=dt*deltaLen/timeToClose
    
    #desireFrac=min(sepMag/desiredLen,20.0)

    #print "DesFrac:", desireFrac
    
    movementVec=separation.norm().mul(closeSpeed)

    #print "movementVec:", movementVec
    
    #gCameraPos=gCameraPos.add(movementVec)
    gCameraPos=idealPos

def main():
    global gPosList
    global dots

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()

    try:
        surface = pygame.display.set_mode(SCREEN_SIZE, video_flags)
    except pygame.error:
        print("I only know about the following modes:")
        print(pygame.display.list_modes())
        print("and of those, only the following fit our flags:")
        print(pygame.display.list_modes(0, video_flags))
        return

    if swap_control:
        if 'wglInitSwapControlARB' in globals():
            wglInitSwapControlARB()

        if 'wglSwapIntervalEXT' in globals():
            print("setting swap control")
            if wglSwapIntervalEXT(0):
                print("swap control set to 0")
            else:
                print("swap control not set")
        else:
            print("swap control function not available")
    else:
        print("cannot set vsync")

    resize(*SCREEN_SIZE)

    pygame.display.set_caption("fanciful flight sim")

    init()

    print("texture units:", glGetIntegerv(GL_MAX_TEXTURE_UNITS_ARB))

    frames = 0
    ticks = pygame.time.get_ticks()
    myClock=pygame.time.Clock()

    points=[Vec3f(   0.0,    0.0,  0.0),
            Vec3f(-270.0,    0.0,  0.0),
            Vec3f( -23.0, -160.0,  0.0)]

    global gPlane
    gPlane=plane.PlaneObj()

    for p in points:
        gMesas.append(makeMap.makeSeussMesa(p))

    newTarget=target.Target()
    newTarget.pos=Vec3f(130.0, 70.0, 50.0)
    
    gTargets.append(newTarget)

    newTarget=target.Target()
    newTarget.pos=Vec3f(-130.0, -70.0, 50.0)

    gTargets.append(newTarget)
    

    myClock.tick()


    gameOver=0

    
    while not gameOver:
        ms=myClock.tick(100)
        tm=pygame.time.get_ticks()

        global gTime

        gTime=tm/1000.0

        event = pygame.event.poll()

        if event.type == QUIT:
            break
        else:
            handleEvent(event)

        #update
        deltaT=ms/1000.0
        updateCamera(deltaT)
        gPlane.tickPhysics(deltaT)

        mx,my=pygame.mouse.get_pos()

        gPlane.steer(mx/float(SCREEN_SIZE[0]),
                     my/float(SCREEN_SIZE[1]))

        if (not dots) or tm-dots[-1][0]>100:
            dots.append((tm,gPlane.pos.mul(1.0)))
            if len(dots)>50:
                dots=dots[-50:]

        for t in gTargets:
            if t.isInside(gPlane.pos):
                if not gPosList:
                    gameOver=1
                else:
                    t.pos=gPosList[0]
                    gPosList=gPosList[1:]
        

        draw()

        pygame.time.wait(2)
        pygame.display.flip()
        frames = frames+1
        

    minutes,seconds=divmod(gTime,60.0)
        
    print("elapsedTime: %d:%02d" % (int(minutes), int(seconds)))
    print("fps:  %d" % int((frames*1000)/(pygame.time.get_ticks()-ticks)))


if __name__ == '__main__': main()
    
