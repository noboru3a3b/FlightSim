import MeatEngine.Math.vector

class DirectionalLight:
    def __init__(self, lightDir, color):
        self.dir=lightDir
        self.color=color

class PointLight:
    def __init__(self, lightPos, color):
        self.pos=lightPos
        self.color=color
