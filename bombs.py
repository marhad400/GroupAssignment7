from inherited import Bomb

import random

class BombMaster:
    
    def __init__(self):
        self.bomb_list: list[Bomb] = []

    def create_bomb(self, screen_size, vel):

        params: dict = {
            'x': random.randint(40, screen_size[0] - 40),
            'y': (screen_size[1] - 40),
            'v_y': int(vel),
            'size': 40
        }

        bomb = Bomb
        created_bomb = bomb(**params)

        self.bomb_list.append(created_bomb)

    def draw_all(self, surface):
        [bomb.draw(surface) for bomb in self.bomb_list]

    def move_all(self, screen_size):
        [bomb.move(screen_size, grav=2) for bomb in self.bomb_list]

    def remove_exploded(self):
        for bomb in self.bomb_list:
            if bomb.explode():
                self.bomb_list.remove(bomb)