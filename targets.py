from abstract import Drawable
from inherited import Target, MovingTarget

import random

class TargetMaster:

    def __init__(self):
        self.target_list: list[Drawable] = []

    def create_random_target(self, screen_size, target_size, is_moving: bool | None = None):
        is_moving = is_moving if is_moving is not None else bool(random.randint(0, 1))

        moving_target_type = [
            MovingSquare, 
            MovingTriangle, 
            MovingCircle 
        ]
        static_target_type = [
            StaticSquare,
            StaticTriangle,
            StaticCircle
        ]

        chosen_type: Drawable = None
        params: dict = {
            'x': random.randint(target_size, screen_size[0] - target_size),
            'y': random.randint(target_size, screen_size[1] - target_size),
            'size': target_size
        }
        if is_moving:
            chosen_type = random.choice(moving_target_type)
        else:
            chosen_type = random.choice(static_target_type)
        
        created_target = chosen_type(**params)
        self.target_list.append(created_target)

    def draw_all(self, surface):
        [target.draw(surface) for target in self.target_list]
    
    def move_all(self):
        [target.move() for target in self.target_list if isinstance(target, MovingTarget)]

class MovingSquare(MovingTarget):
    
    def __init__(self, x, y, v_x=None, v_y=None, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            v_x = v_x, v_y = v_y, 
            color = color, size = size, health = health, 
            shape = 's')

class MovingTriangle(MovingTarget):
    def __init__(self, x, y, v_x=None, v_y=None, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            v_x = v_x, v_y = v_y, 
            color = color, size = size, health = health, 
            shape = 't')

class MovingCircle(MovingTarget):
    def __init__(self, x, y, v_x=None, v_y=None, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            v_x = v_x, v_y = v_y, 
            color = color, size = size, health = health, 
            shape = 'c')

class StaticSquare(Target):
    def __init__(self, x, y, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            color = color, size = size, health = health, 
            shape = 's')

class StaticTriangle(Target):
    def __init__(self, x, y, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            color = color, size = size, health = health, 
            shape = 't')

class StaticCircle(Target):
    def __init__(self, x, y, color=None, size=None, health=None):
        super().__init__(
            x = x, y = y, 
            color = color, size = size, health = health, 
            shape = 'c')