""" this is the thing you want to hit

"""

import math
from OpenGL.GL import *
from OpenGL.GLU import *

from MeatEngine.Math.vector import Vec3f


class Target:
    def __init__(self):
        self.pos=Vec3f(0.0, 0.0, 0.0)

        self.blinkRate=1.5

        self.color1=(0.0, 0.25, 0.0)
        self.color2=(0.75, 1.0, 0.75)

        self.size=10.0


    def draw(self, timeNow):
        dummy, blinkDur=divmod(timeNow,self.blinkRate)
        blinkFrac=blinkDur/self.blinkRate
        sawTooth=blinkFrac*2.0
        if sawTooth>1.0:
            sawTooth=2.0-sawTooth

        c=[self.color1[i]+sawTooth*(self.color2[i]-self.color1[i])
           for i in range(3)]

        glColor3f(*c)

        x=self.pos.x
        y=self.pos.y
        z=self.pos.z
        s=self.size
        
        glBegin(GL_LINE_LOOP)
        glVertex3f(x-s, y-s, z-s)
        glVertex3f(x+s, y-s, z-s)
        glVertex3f(x+s, y+s, z-s)
        glVertex3f(x-s, y+s, z-s)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        glVertex3f(x-s, y-s, z+s)
        glVertex3f(x+s, y-s, z+s)
        glVertex3f(x+s, y+s, z+s)
        glVertex3f(x-s, y+s, z+s)
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(x-s, y-s, z-s)
        glVertex3f(x-s, y-s, z+s)
        glVertex3f(x+s, y-s, z-s)
        glVertex3f(x+s, y-s, z+s)
        glVertex3f(x+s, y+s, z-s)
        glVertex3f(x+s, y+s, z+s)
        glVertex3f(x-s, y+s, z-s)
        glVertex3f(x-s, y+s, z+s)
        glEnd()


    def isInside(self, pos):
        return (pos.x>self.pos.x-self.size and
                pos.y>self.pos.y-self.size and
                pos.z>self.pos.z-self.size and
                pos.x<self.pos.x+self.size and
                pos.y<self.pos.y+self.size and
                pos.z<self.pos.z+self.size)

        

        
