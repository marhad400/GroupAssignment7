from inherited import Bomb

import random

class BombMaster:
    
    def __init__(self):
        self.bomb_list: list[Bomb] = []

    def create_bomb(self, screen_size, v_y):

        params: dict = {
            'x': random.randint(40, screen_size[0] - 40),
            'y': (40),
            'v_y': int(v_y),
            'size': 40
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