from random import randint

class Color:
    """A class containing (R, G, B) tuple definitions for a variety of colors."""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (50, 100, 230)
    GRAY = (128, 128, 128)

    @staticmethod
    def rand_color() -> tuple:
        """Returns a random color by choosing three RGB values from 5-255"""
        return (randint(5, 255), randint(5, 255), randint(5, 255))