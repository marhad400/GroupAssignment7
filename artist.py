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
        surface : pygame.Surface
            The surface to draw the object onto
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
            # Polygon draw takes 2 coords of the points of the triangle
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
    def draw_cannon(
            surface: pygame.Surface, 
            x: int, 
            y: int, 
            angle: int, pow: int, 
            color: tuple) -> None:
        """
        Draws the cannon based on its parameters

        This function uses the angle and power to determine the size and angle
        of the cannon

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the cannon onto
        x : int
            The x coordinate of the object
        y : int 
            The y coordinate of the object
        angle : int
            The cannon's angle
        pow : int
            The power of the cannon (depending on how long the user held for)
        color : tuple
            A tuple representing the (R, G, B) values of the object's color
        """

        vec_1 = np.array(
                [
                int(5*np.cos(angle - np.pi/2)), 
                int(5*np.sin(angle - np.pi/2))
                ]
            )
        vec_2 = np.array(
                [
                    int(pow*np.cos(angle)), 
                    int(pow*np.sin(angle))
                ]
            )
        
        gun_pos = np.array([x, y])
        
        # Determine the gun's shape (a polygon needs a list of points)
        # Even though this will come out as a rectangle, we just get its list
        # of points as a polygon and draw that
        gun_shape = []
        gun_shape.append(
            (gun_pos + vec_1).tolist()
        )
        gun_shape.append(
            (gun_pos + vec_1 + vec_2).tolist()
        )
        gun_shape.append(
            (gun_pos + vec_2 - vec_1).tolist()
        )
        gun_shape.append(
            (gun_pos - vec_1).tolist()
        )
        
        pygame.draw.polygon(surface, color, gun_shape)

    @staticmethod
    def draw_score(
            surface: pygame.Surface, 
            font: pygame.font.Font, 
            targets_destroyed: int, 
            projectiles_used: int, 
            score: int, 
            chosen_type : str,
            primary_color: tuple, 
            secondary_color: tuple) -> None:
        """
        Draws the score table based on its parameters

        This function uses the font, scores, and colors to draw the score table

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the cannon onto
        font : pygame.font
            The font to use for the text
        targets_destroyed : int
            The number of targets destroyed by the player
        projectiles_used : int
            The number of projectiles used
        score : int
            The player's total score, determined by targets and projectiles
        chosen_type : str
            The user's currently chosen type
        primary_color : tuple
            The color to use for the score
            The color to use for the statistics
        secondary_color : tuple
            The color to use for the statistics
        """
        score_surf = []
        
        # The text for targets_destroyed
        score_surf.append(
            font.render(
                "Destroyed: {}".format(targets_destroyed), 
                True, 
                secondary_color
            )
        )

        # The text for projectiles_used
        score_surf.append(
            font.render(
                "Balls used: {}".format(projectiles_used), 
                True, 
                secondary_color
            )
        )

        # The text for the total score
        score_surf.append(
            font.render(
                "Total: {}".format(score), 
                True, 
                primary_color
            )
        )

        # The test for the chosen type
        if chosen_type == 's':
            chosen_type = "Square"
        if chosen_type == 'c':
            chosen_type = "Circle"
        if chosen_type == 't':
            chosen_type = "Triangle"
        
        score_surf.append(
            font.render(
                f"Chosen: {chosen_type}",
                True,
                primary_color
            )
        )

        # Place each text piece to the screen
        for i in range(3):
            surface.blit(
                score_surf[i], 
                [10, 10 + 30*i]\
            )
        
        surface.blit(score_surf[-1], [surface.get_size()[1] - 50, 10])