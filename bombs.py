from abstract import Drawable, Killable, Moveable
from artist import Artist
from pygame import Surface
from color import Color


class BombMaster:
    
    def __init__(self):
        self.bomb_list: list[Bomb] = []

    def create_bomb(self, x, y, v_y):

        params: dict = {
            'x': x,
            'y': y,
            'v_y': v_y,
            'size': 30
        }

        created_bomb = Bomb(**params)

        self.bomb_list.append(created_bomb)

    def draw_all(self, surface):
        [bomb.draw(surface) for bomb in self.bomb_list]

    def move_all(self):
        [bomb.move(grav=2) for bomb in self.bomb_list]

    def remove_exploded(self):
        for bomb in self.bomb_list:
            if bomb.is_alive():
                self.bomb_list.remove(bomb)
    
class Bomb(Drawable, Killable, Moveable):
    def __init__(
            self, 
            x: int, 
            y: int, 
            v_y: int = None,
            v_x: int = 0,  
            size: int = 40, 
            health: int = 1,
            color: int = None, 
            shape: int = 'c') -> None:
        
        color = color or Color.RED

        # Parent class initialization
        Drawable.__init__(self, x, y, color=color, size=size)
        Killable.__init__(self, health=health)
        Moveable.__init__(self, v_y=v_y, v_x=v_x)
        # Shape initialization
        self.shape = shape
    
    def move(self, time: int = 1, grav: int = 0) -> None:
        
        #Add gravity
        self.v_y += grav

        # Change y-position based on gravity
        self.y += time * self.v_y

    def draw(self, surface: Surface) -> None:

        Artist.draw(
            surface,
            self.x, self.y,
            self.color, self.size, self.shape
        )
    
    def check_bottom(self, screen_size):
        
        #If the projectile reaches the bottom of the screen
        at_bottom = False
        if self.y < screen_size[1] -self.size:
            at_bottom = True

        return at_bottom
    
    def explode(self, screen_size):
        if self.check_bottom(screen_size):
            self.kill()