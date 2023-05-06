from abstract import Drawable, Killable, Moveable
from color import Color


class Target(Drawable, Killable):
    def __init__(self, color=Color.rand_color(), size=5, health=100):
        Drawable.__init__(self, color=color, size=size)
        Killable.__init__(self, health=health)

class MovingTarget(Moveable, Target):
    def __init__(self, x, y, v_x, v_y, color=None, size=None, health=None):
        Moveable.__init__(self, x, y, v_x, v_y)
        Target.__init__(color, size, health)

class Projectile(Drawable, Killable, Moveable):
    def __init__(self, x, y, v_x, v_y, color=None, size=None, health=None):
        Drawable.__init__(self, color=color, size=size)
        Killable.__init__(self, health=health)
        Moveable.__init__(self, x, y, v_x, v_y)