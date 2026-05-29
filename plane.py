"""plane physics model"""

import math
from OpenGL.GL import *
from OpenGL.GLU import *

import model
from MeatEngine.Math.vector import Vec3f

def makePlaneModel():
    m=model.Model()

    length=10.0
    width=2.0
    height=2.0
    
    m.verts=[Vec3f(0.0, length, 0.0),
             Vec3f(-width*3.0, -length, height),
             Vec3f(-width, -length, height),
             Vec3f(   0.0, -length, -height),
             Vec3f( width, -length, height),
             Vec3f( width*3.0, -length, height)]

    m.lines=[(0,1),
             (0,2),
             (0,3),
             (0,4),
             (0,5),
             (1,2),
             (2,3),
             (3,4),
             (4,5)]

    triIndices=[(0,1,2),
                (0,2,3),
                (0,3,4),
                (0,4,5)]

    m.tris=[{'color':(1.0, 1.0, 1.0), 'indices':t} for t in triIndices]

    return m
             

class PlaneObj:
    def __init__(self):
        self.visualModel=makePlaneModel()
        self.pos=Vec3f(70.0, 70.0, 30.0)

        self.heading=135.0
        self.roll=0.0
        self.pitch=0.0

        self.bankRate=0.5
        self.riseRate=0.8
        self.accelerationRate=1.0
        
        self.velocity=30.0

        self.minSpeed=5.0
        self.maxSpeed=50.0

    def steer(self, fx, fy):
        fx=2.0*fx-1.0
        fy=2.0*fy-1.0

        self.roll=60.0*fx
        self.pitch=15.0*fy

    def tickPhysics(self, dt):
        # a negative roll leads to a positive delta heading
        self.heading -= self.bankRate*self.roll*dt

        # a negative pitch is a positive acceleration
        self.velocity -= self.accelerationRate*self.pitch*dt

        self.velocity=min(self.maxSpeed,self.velocity)
        self.velocity=max(self.minSpeed,self.velocity)
        
        self.pos.z += self.riseRate*self.pitch*dt

        radians=math.radians(self.heading)
        dx=self.velocity*math.cos(radians)
        dy=self.velocity*math.sin(radians)

        self.pos.x+=dx*dt
        self.pos.y+=dy*dt

    def draw(self):
        # set the camera position

        glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()

        glTranslatef(self.pos.x,
                     self.pos.y,
                     self.pos.z)

        glRotatef(self.heading-90.0,  0.0, 0.0, 1.0)
        glRotatef(self.pitch,    1.0, 0.0, 0.0)
        glRotatef(self.roll,     0.0, 1.0, 0.0)

        glBegin(GL_TRIANGLES)
        for t in self.visualModel.tris:
            glColor3f(*t['color'])
        
            for vi in t['indices']:
                v=self.visualModel.verts[vi]
                glVertex3f(v.x, v.y, v.z)
        glEnd()
            
        
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for i1, i2 in self.visualModel.lines:
            v1=self.visualModel.verts[i1]
            v2=self.visualModel.verts[i2]
    
            for v in (v1,v2):
                glVertex3f(v.x, v.y, v.z)
        glEnd()
        


    
