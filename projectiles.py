from inherited import Projectile

import random
import numpy as np

class ProjectileMaster:

    def __init__(self):
        self.projectile_list: list[Projectile] = []

    def create_random_projectile(self, x, y, vel, angle):

        projectile_types = [
            CircleProjectile,
            SquareProjectile,
            TriangleProjectile
        ]

        chosen_type: Projectile = None
        params: dict = {
            'x': x,
            'y': y,
            'size': 20,
            'v_x': int(vel * np.cos(angle)),
            'v_y': int(vel * np.sin(angle))
        }
        
        chosen_type = random.choice(projectile_types)
        created_projectile = chosen_type(**params)
        
        self.projectile_list.append(created_projectile)

    def draw_all(self, surface):
        [projectile.draw(surface) for projectile in self.projectile_list]
    
    def move_all(self, screen_size):
        [projectile.move(screen_size, grav=2) for projectile in self.projectile_list]
    
    def remove_dead(self):
        for projectile in self.projectile_list:
            if not projectile.is_alive:
                self.projectile_list.remove(projectile)

class CircleProjectile(Projectile):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 'c')

class SquareProjectile(Projectile):
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 's')
        
class TriangleProjectile(Projectile):
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 't')