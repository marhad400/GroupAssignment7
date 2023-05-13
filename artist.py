import pygame

import numpy as np

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
            'c': ((x, y), size/2, pygame.draw.circle),
        }[shape[0]] # Choose which shape to draw and function to use depending on the
        # first character of the passed string

        # Run the given function with the given parameters
        function_to_use(surface, color, *shape_to_draw)
    
    @staticmethod
    def draw_cannon(surface, x, y, angle, pow, color):
        gun_shape = []
        vec_1 = np.array([int(5*np.cos(angle - np.pi/2)), int(5*np.sin(angle - np.pi/2))])
        vec_2 = np.array([int(pow*np.cos(angle)), int(pow*np.sin(angle))])
        gun_pos = np.array([x, y])
        
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        
        pygame.draw.polygon(surface, color, gun_shape)

    @staticmethod
    def draw_score(surface, font, targets_destroyed, projectiles_used, score, primary_color, secondary_color):
        score_surf = []
        score_surf.append(font.render("Destroyed: {}".format(targets_destroyed), True, primary_color))
        score_surf.append(font.render("Balls used: {}".format(projectiles_used), True, primary_color))
        score_surf.append(font.render("Total: {}".format(score), True, secondary_color))
        for i in range(3):
            surface.blit(score_surf[i], [10, 10 + 30*i])