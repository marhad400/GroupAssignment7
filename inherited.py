from abstract import Drawable, Killable, Moveable
from color import Color

from artist import Artist

import random

class GameObject(Moveable, Drawable):
    def __init__(self): pass

class Target(Drawable, Killable):
    def __init__(self, x, y, color = None, size = None, health = None, shape = None):
        color = color or Color.rand_color()
        size = size or 5
        health = health or 1
        shape = shape or 'c'
        
        Drawable.__init__(self, x=x, y=y, color=color, size=size)
        Killable.__init__(self, health=health)
        self.shape = shape
    
    def draw(self, s):
        Artist.draw(s, self.x, self.y, self.shape, self.color, self.size)
    
    def check_collision(self, ball):
        dist = sum([(self.x - ball.x)**2, (self.y - ball.y)**2])**0.5
        min_dist = self.size + ball.size
        return dist <= min_dist

    def __str__(self):
        return f"Static Target of Shape({self.shape}), " \
                f"Pos({self.x}, {self.y}), " \
                f"Color({self.color}), Size({self.size}), Health({self.health})"
            
    def __repr__(self):
        return self.__str__()

class MovingTarget(Moveable, Target):
    def __init__(self, x, y, v_x = None, v_y = None, color = None, size = None, health = None, shape = None):
        v_x = random.randint(-2, 2)
        v_y = random.randint(-2, 2)
        color = color or Color.rand_color()
        size = size or 30
        health = health or 1

        Moveable.__init__(self, v_x, v_y)
        Target.__init__(self, x, y, color, size, health, shape)
    
    def move(self):
        self.x += self.v_x
        self.y += self.v_y
    
    def __str__(self):
        return f"Moving Target of Shape({self.shape}), " \
                f"Pos({self.x}, {self.y}), " \
                f"Color({self.color}), Size({self.size}), Health({self.health}), " \
                f"Speed({self.v_x}, {self.v_y})"
    
    def __repr__(self):
        return self.__str__()

class Projectile(Drawable, Killable, Moveable):
    def __init__(self, x, y, v_x, v_y, color, size, health, shape):
        color = color or Color.rand_color()
        size = size or 5
        health = health or 1
        shape = shape or 'c'

        Drawable.__init__(self, x, y, color=color, size=size)
        Killable.__init__(self, health=health)
        Moveable.__init__(self, v_x, v_y)
        self.shape = shape

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        coords = [self.x, self.y]
        vels = [self.v_x, self.v_y]
        for i in range(2):
            if coords[i] < self.size:
                coords[i] = self.size
                vels[i] = -int(vels[i] * refl_ort)
                vels[1-i] = int(vels[1-i] * refl_par)
            elif coords[i] > Color.SCREEN_SIZE[i] - self.size:
                coords[i] = Color.SCREEN_SIZE[i] - self.size
                vels[i] = -int(vels[i] * refl_ort)
                vels[1-i] = int(vels[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to it's velocity and time step.
        Changes the ball's velocity due to gravitational force.
        '''
        self.v_y += grav
        self.x += time * self.v_x
        self.y += time * self.v_y
        self.check_corners()
        if self.v_x**2 + self.v_y**2 < 2**2 and self.y > Color.SCREEN_SIZE[1] - self.size:
            self.is_alive = False

    def draw(self, s):
        Artist.draw(s, self.x, self.y, self.shape, self.color, self.size)