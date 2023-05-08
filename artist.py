import pygame

from color import Color

class Artist:

    @staticmethod
    def draw(surface, x, y, shape, color, size):
        
        *shape_to_draw, function_to_use = {
            's': ((x, y, size, size), pygame.draw.rect),
            't':  ((
                    (x, y), 
                    (x - size//2, y + size//2),
                    (x + size//2, y + size//2)
                ), pygame.draw.polygon),
            'c': ((x, y), size, pygame.draw.circle),
        }[shape[0]]


        function_to_use(surface, color, *shape_to_draw)