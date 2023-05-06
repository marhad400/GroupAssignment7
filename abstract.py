class Drawable:

    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(): pass

class Moveable:

    def __init__(self, x, y, v_x, v_y):
        self.x, self.y = x, y
        self.v_x, self.v_y = v_x, v_y
    
    def move(): pass

class Killable:

    def __init__(self, health):
        self.health = health
    
    def deal(self, damage):
        self.health -= damage
    
    def heal(self, health):
        self.health += health

    def is_alive(self):
        return self.health > 0