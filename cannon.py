import numpy as np
from color import Color
from abstract import Moveable, Drawable, Killable
from artist import Artist
from projectiles import ProjectileMaster

import time
import threading

class Cannon(Drawable, Killable):

    def __init__(self, x, y, health=1, color=None, angle=0, max_pow=50, min_pow=10):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        color = color or Color.rand_color()

        Drawable.__init__(self, x=x, y=y, color=color, size=1)
        Killable.__init__(self, health=health)

        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow

        self.active = False
        self.pow = min_pow

        self.chosen_type = 'c'

        self.projectile_master = ProjectileMaster()

    def change_chosen(self, chosen):
        self.chosen_type = chosen

    def activate(self):
        '''
        Activates gun's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current gun charge power.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self, vel = None):
        '''
        Creates ball, according to gun's direction and current charge power.
        '''
        vel = vel or self.pow
        
        self.projectile_master.create_projectile(self.x, self.y, vel, self.angle, self.chosen_type)
        self.pow = self.min_pow
        self.active = False
                
    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(target_pos[1] - self.y, target_pos[0] - self.x)

    def draw(self, screen):
        '''
        Draws the gun on the screen.
        '''
        Artist.draw_cannon(screen, self.x, self.y, self.angle, self.pow, self.color)

class MovingCannon(Moveable, Cannon):
    
    def __init__(self, v_x=6, v_y=6, *args, **kwargs):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''

        Moveable.__init__(self, v_x=v_x, v_y=v_y)
        Cannon.__init__(self, *args, **kwargs)

    def move(self, screen_size: tuple, move_x: int = 0, move_y: int = 0):
        '''
        Changes vertical position of the gun.
        '''
        self.x += move_x * self.v_x
        self.x = max(30, min(self.x, screen_size[0] - 30))
        
        self.y += move_y * self.v_y
        self.y = max(30, min(self.y, screen_size[1] - 30))
    
    def move_right(self, screen_size):
        self.move(screen_size, 1, 0)

    def move_left(self, screen_size):
        self.move(screen_size, -1, 0)
    
    def move_up(self, screen_size):
        self.move(screen_size, 0, -1)
    
    def move_down(self, screen_size):
        self.move(screen_size, 0, 1)

class ArtificialCannon(MovingCannon):
    '''
    Tank class. Manages its renderring, movement, and striking. 
    '''
    def __init__(self, v_x = 3, v_y = 3, min_pow = 30, *args, **kwargs):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        super().__init__(v_x, v_y, min_pow = min_pow, *args, **kwargs)

        self.strike_thread = None

    def determine_move(self, user_cannon, screen_size):
        d_x = self.x - user_cannon.x
        d_y = self.y - user_cannon.y

        dist = sum(
                    [
                        (self.x - user_cannon.x)**2, 
                        (self.y - user_cannon.y)**2
                    ]
                )**0.5
        min_dist = self.size + user_cannon.size + 100
        
        if dist < min_dist:
            return False

        if d_x < 0:
            self.move_right(screen_size)
        elif d_x > 0:
            self.move_left(screen_size)
        
        if d_y < 0:
            self.move_down(screen_size)
        elif d_y > 0:
            self.move_up(screen_size)

        return True

    def keep_striking(self):
        while self.strike_thread:
            time.sleep(0.5)
            if self.strike_thread:
                self.strike(vel=60)

    def start_thread(self):
        if not self.strike_thread:
            self.strike_thread = threading.Thread(target=self.keep_striking, daemon=True)
            self.strike_thread.start()
        
    def end_thread(self):
        self.strike_thread = None
