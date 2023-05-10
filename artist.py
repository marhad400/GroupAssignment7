import pygame

from color import Color

class Artist:
    """A class containing static definitions for draw functions

    Allows for a factory of artistry, dedicated to drawing objects based on
    their provided coordinates, color, shape, and size
    """

    @staticmethod
    def draw(
            surface: pygame.Surface, 
            x: int, 
            y: int, 
            color: tuple, 
            size: int,
            shape: str) -> None: 
        """
        Draws the object based on its parameters

        This function uses a dictionary to store shape: parameter, functions.
        The shape is one of 's', 't', or 'c' signifying square, triangle, or circle.
        The parameters is a tuple of the parameters that are to be passed to the
        respective pygame.draw function.

        Parameters
        ----------
        x : int
            The x coordinate of the object
        y : int 
            The y coordinate of the object
        color : tuple
            A tuple representing the (R, G, B) values of the object's color
        size : int
            An int representing the size of the object
            For a square, it will be the length of a side
            For a circle, it will be its radius
            For a triangle, it will be the length of a side
        shape : str
            A string of characters 's', 't', or 'c' denoting whether the object is a
            square, triangle, or circle.
        """
        *shape_to_draw, function_to_use = {
            # Rectangle draw takes coords and side lengths
            's': ((x, y, size, size), pygame.draw.rect),
            # Polygon draw takes coords of the points of the polygon (3 for triangle)
            't':  ((
                    (x, y), 
                    (x - size//2, y + size//2),
                    (x + size//2, y + size//2)
                ), pygame.draw.polygon),
            # Circle draw takes a tuple of coords and a radius
            'c': ((x, y), size, pygame.draw.circle),
        }[shape[0]] # Choose which shape to draw and function to use depending on the
        # first character of the passed string

        # Run the given function with the given parameters
        function_to_use(surface, color, *shape_to_draw)