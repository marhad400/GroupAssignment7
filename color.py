from random import randint

class Color:
    
    WHITE = (255, 25, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    SCREEN_SIZE = (800, 600)

    @staticmethod
    def rand_color() -> tuple:
        return (randint(0, 255), randint(0, 255), randint(0, 255))