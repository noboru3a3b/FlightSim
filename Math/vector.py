"""Meat Engine Vector Library

Provides vectors of 2 and 3 dimensions
"""
import math



class Vec2f:
    def __init__(self, x,y):
        """Vector constructor"""
        self.x=x
        self.y=y

    def add(self, v):
        """Vector Addiction"""
        return Vec2f(self.x+v.x,
                     self.y+v.y)

    def sub(self, v):
        """Vector Subtraction

        returns self-v"""
        return Vec2f(self.x-v.x,
                     self.y-v.y)

    def mul(self, s):
        """Scalar Multiplication
        
        returns self*s (scalar multiplication)
        """

        return Vec2f(self.x*s,
                     self.y*s)

    def dot(self, v):
        """Dot product."""
        return self.x*v.x+self.y*v.y

    def mag(self):
        """length
        
        return the magnitude(length) of the vector.
        """
        return math.sqrt(self.magSqr())
        pass

    def magSqr(self):
        """Square of the magnitude.
        
        this is faster than calling mag(), and is often just as useful.
        """
        return (self.x*self.x+
                self.y*self.y)

    def norm(self):
        """normalize
        
        returns a unit vector in the same direction as this vector.
        """
        m=self.mag()
        return Vec2f(self.x/m,
                     self.y/m)

    def __str__(self):
        return "[%0.3f %0.3f]"%(self.x, self.y)

    def __repr__(self):
        return "<Vec3f %s>"%(str(self))


    def samePoint(self, v1, epsilon):
        return self.sub(v1).mag()<=epsilon

    



class Vec3f:
    def __init__(self, x,y,z):
        """Vector constructor"""
        self.x=x
        self.y=y
        self.z=z

    def add(self, v):
        """Vector Addiction"""
        return Vec3f(self.x+v.x,
                     self.y+v.y,
                     self.z+v.z)

    def sub(self, v):
        """Vector Subtraction

        returns self-v"""
        return Vec3f(self.x-v.x,
                     self.y-v.y,
                     self.z-v.z)

    def mul(self, s):
        """Scalar Multiplication
        
        returns self*s (scalar multiplication)
        """

        return Vec3f(self.x*s,
                     self.y*s,
                     self.z*s)

    def dot(self, v):
        """Dot product."""
        return self.x*v.x+self.y*v.y+self.z*v.z

    def cross(self, v):
        """Cross product.

        self cross v
        """
        
        return Vec3f(self.y*v.z-self.z*v.y,
                     self.z*v.x-self.x*v.z,
                     self.x*v.y-self.y*v.x)

    def mag(self):
        """length
        
        return the magnitude(length) of the vector.
        """
        return math.sqrt(self.magSqr())
        pass

    def magSqr(self):
        """Square of the magnitude.
        
        this is faster than calling mag(), and is often just as useful.
        """
        return (self.x*self.x+
                self.y*self.y+
                self.z*self.z)

    def norm(self):
        """normalize
        
        returns a unit vector in the same direction as this vector.
        """
        m=self.mag()
        return Vec3f(self.x/m,
                     self.y/m,
                     self.z/m)

    def __str__(self):
        return "[%0.3f %0.3f %0.3f]"%(self.x, self.y, self.z)

    
