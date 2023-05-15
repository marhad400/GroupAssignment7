from abstract import Drawable, Killable, Moveable
from artist import Artist
from pygame import Surface
from color import Color

import random

class BombMaster:
    """
    Implements methods for target-wide bomb checking

    Introduces methods for creating bombs and maintaining existing 
    bombs (drawing them and moving them)
    
    Attributes
    ----------
    bomb_list : list[Bomb]
        A list of all the bombs created by this BombMaster
    """

    def __init__(self) -> None:
        """Initializes the empty bombs list"""
        self.bomb_list: list[Bomb] = []

    def create_bomb(
            self, 
            x: int, 
            y: int, 
            v_y: int, 
            chance: float = 1) -> None:
        """
        Creates a bomb at the target's position given a few parameters
    
        This function only stores the bomb in the bombs list, doesn't return it

        Parameters
        ----------
        x : int
            The x position of the target
        y : int
            The y position of the target
        v_y : int
            The initial y velocity of the bomb (it will be affected by gravity)
        chance : float
            The decimal chance of the target creating a bomb (default 1) 
        """

        # If the chance to drop a bomb is too high
        if random.random() > chance:
            return 

        # The bomb's parameters
        params: dict = {
            'x': x,
            'y': y,
            'v_y': v_y,
        }

        # Create and store the bomb
        created_bomb = Bomb(**params)
        self.bomb_list.append(created_bomb)

    def draw_all(self, surface: Surface) -> None:
        """
        Simply loops through all the bombs and draws them to the surface
        
        Simply calls the bomb.draw function on each bomb

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the bomb to
        """
        [bomb.draw(surface) for bomb in self.bomb_list]

    def move_all(self) -> None:
        """
        Simply loops through all the bombs and moves them
          
        Moves them by calling bomb.move function on each bomb
        """
        [bomb.move(gravity=2) for bomb in self.bomb_list]

    def remove_exploded(self, screen_y: int, user: Drawable) -> None:
        """
        Removes the dead bombs from the list
        
        Parameters
        ----------
        screen_y : int
            The y position of the screen
        user : Drawable
            A Drawable object that is the user
        """
        for bomb in self.bomb_list:
            bomb.check_explode(screen_y, user)
            if not bomb.is_alive:
                self.bomb_list.remove(bomb)
    
class Bomb(Drawable, Killable, Moveable):
    """
    A class representing a bomb

    When a bomb falls on the player, it instantly kills them.

    A Bomb is a Drawable (meaning it can be drawn to the screen) and is Killable
    (meaning it can take damage and die). This means we need to pass in all the
    attributes necessary for both a Drawable and Killable object, and an 
    attribute for the shape. In addition, bombs can be dropped/moved 
    (making it a Moveable as well).
    
    Attributes
    ----------
    x : int
        The x coordinate of the object
    y : int 
        The y coordinate of the object
    v_y : int
        The downwards velocity of the bomb (affected by gravity)
    size : int
        An int representing the size of the object
        For a square, it will be the length of a side
        For a circle, it will be its radius
        For a triangle, it will be the length of a side
    health : int
        An int denoting the object's health. A health value of 1 means the object
        is killed after a single hit.
    color : tuple
        A tuple representing the (R, G, B) values of the object's color
    shape : str
        A string of characters 's', 't', or 'c' denoting whether the object is a
        square, triangle, or circle (default 'c')
    """

    def __init__(
            self, 
            x: int, 
            y: int, 
            v_y: int = None,  
            size: int = 30, 
            health: int = 1,
            color: int = None, 
            shape: int = 'c') -> None:
        
        color = color or Color.RED

        # Parent class initialization
        Drawable.__init__(self, x = x, y = y, color = color, size = size)
        Killable.__init__(self, health = health)
        Moveable.__init__(self, v_x = 0, v_y = v_y)
        # Shape initialization
        self.shape = shape
    
    def move(self, time: int = 1, gravity: int = 0) -> None:
        """
        Moves the bomb based on its velocity and gravity

        Parameters
        ----------
        time : int
            The rate of time (default 1)
        gravity : int
            The rate of gravity (default 0)
        """
        # Add gravity
        self.v_y += gravity

        # Change y-position based on time
        self.y += time * self.v_y

    def draw(self, surface: Surface) -> None:
        """
        Draws the bomb by delgating to the default Artist.draw function

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the bomb onto
        """
        Artist.draw(
            surface,
            self.x, self.y,
            self.color, self.size, self.shape
        )
    
    def check_bottom(self, screen_y: int) -> bool:
        """
        Checks if the bomb has reached the bottom of the screen

        Parameters
        ----------
        screen_y : int
            The y position of the bottom of the screen 
        
        Returns
        -------
        at_bottom : bool
            Whether or not the bomb is at the bottom of the screen
        """
        return self.y >= screen_y - self.size
    
    def check_user(self, user: Drawable) -> bool:
        """
        Checks if the bomb has reached the user

        Parameters
        ----------
        user : Drawable
            A Drawable object that is the user cannon

        Returns
        -------
        at_user : bool
            Whether or not the bomb is at the user
        """

        return self.check_collision(user)

    def check_explode(self, screen_y: int, user: Drawable) -> None:
        """
        Checks if the bomb needs to explode then explodes the bomb, instantly killing it
        
        Parameters
        ----------
        screen_y : int
            The y position of the bottom of the screen
        """
        at_bottom = self.check_bottom(screen_y)
        at_user = self.check_user(user)
        
        if at_bottom or at_user:
            self.kill()

        if at_user and isinstance(user, Killable):
            user.deal()