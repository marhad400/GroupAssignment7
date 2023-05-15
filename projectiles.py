from abstract import Drawable, Killable, Moveable
from color import Color
from artist import Artist

import random
from math import cos, sin
from pygame import Surface

class ProjectileMaster:
    """
    Implements methods for cannon-wide projectile checking

    Introduces methods for creating random projectiles and maintaining existing 
    projectiles (drawing them and moving them)
    
    Attributes
    ----------
    projectile_list : list[Target]
        A list of all the projectiles created by this ProjectileMaster
    """

    def __init__(self) -> None:
        """Initializes the empty projectile list"""
        self.projectile_list: list[Projectile] = []

    def create_projectile(
            self, 
            x: int, 
            y: int, 
            vel: int, 
            angle: int, 
            chosen_type: str = None) -> None:
        """
        Creates a projectile based on the cannon's parameters

        If a type is not provided, a random projectile will be fired.

        Adds the projectile to the projectile list, does not return it

        Parameters
        ----------
        x : int
            The x position of the projectile.
        y : int 
            The y position of the projectile.
        vel : int
            The velocity of the projectile (determined by the cannon's power)
        angle : int
            The angle of the cannon (affects the v_x and v_y distribution)
        chosen_type : str
            A string of characters 's', 't', or 'c' denoting whether the object is a
            square, triangle, or circle. If it is not provided, it will be random
        """
        
        # The possible projectile types and their chosen_type denotion
        projectile_types = {
            'c': CircleProjectile,
            's': SquareProjectile,
            't': TriangleProjectile
        }

        # The params to create the projectile with
        params: dict = {
            'x': x,
            'y': y,
            'size': 20,
            'v_x': int(vel * cos(angle)),
            'v_y': int(vel * sin(angle))
        }
        
        # A projectile of the chosen type, or a random projectile
        if chosen_type:
            chosen_type = projectile_types[chosen_type]
        else:
            chosen_type = random.choice(list(projectile_types.values()))


        # Create and store the projectile
        created_projectile = chosen_type(**params)
        self.projectile_list.append(created_projectile)

    def draw_all(self, surface: Surface) -> None:
        """
        Simply loops through all the projectiles and draws them to the surface
        
        Simply calls the projectiles.draw function on each target

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the projectiles to
        """
        [projectile.draw(surface) for projectile in self.projectile_list]
    
    def move_all(self, screen_size: tuple) -> None:
        """
        Simply loops through all the projectiles and moves them based on their velocity
        
        Simply calls the projectile.move function on each projectile

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        [projectile.move(screen_size, grav=2) for projectile in self.projectile_list]
    
    def remove_dead(self) -> None:
        """Removes dead projectiles from the projectile list"""
        for projectile in self.projectile_list:
            if not projectile.is_alive:
                self.projectile_list.remove(projectile)

class Projectile(Drawable, Killable, Moveable):
    """A class representing a projectile

    A projectile (which can be one of a square, circle, or triangle) can hit 
    a target of the same shape, or the cannon.

    A Projectile is Drawable, Killable, and Moveable, meaning it needs
    all the attributes for all of those abstract classes.
        
    Attributes
    ----------
    x : int
        The x coordinate of the object
    y : int 
        The y coordinate of the object
    v_x : int
        The object's velocity in the x direction
    v_y : int
        The object's velocity in the y direction
    color : tuple
        A tuple representing the (R, G, B) values of the object's color
    size : int
        An int representing the size of the object
        For a square, it will be the length of a side
        For a circle, it will be its radius
        For a triangle, it will be the length of a side
    health : int
        An int denoting the object's health. A health value of 1 means the object
        is killed after a single hit.
    shape : str
        A string of characters 's', 't', or 'c' denoting whether the object is a
        square, triangle, or circle.
    """

    def __init__(
            self, 
            x: int, 
            y: int, 
            v_x: int, 
            v_y: int, 
            color: int = None, 
            size: int = 5, 
            health: int = 1, 
            shape: int = 'c') -> None:
        """
        Intiailizes the necessary values for a Moveable, Killable, Drawable, 
        object using those classes' init functions 

        While the default value for color, size, health, and shape 
        looks to be None, the function defaults those to a random color, 5, 1, 
        and 'c' for circle. This is due to behavior in Python with passing attributes 
        through super functions.
        """
        color = color or Color.rand_color()

        # Parent class initialization
        Drawable.__init__(self, x, y, color=color, size=size)
        Killable.__init__(self, health=health)
        Moveable.__init__(self, v_x, v_y)
        # Shape initialization
        self.shape = shape

    def move(
            self, 
            screen_size: tuple, 
            time: int = 1, grav: int = 0) -> None:
        """
        Moves the projectile based on its velocity and the effect of gravity

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        time : int
            The time step multiplier for the velocity (default 1)
        gravity : int
            The force of gravity (default 0)
        """
        # Add gravity
        self.v_y += grav

        # Change position based on velocity
        self.x += time * self.v_x
        self.y += time * self.v_y

        # Check screen collisions to make sure we don't go off-screen
        self.check_corners(screen_size)

        # If the projectile is moving slowly at the bottom of the screen
        # it has lost its health
        if self.v_x**2 + self.v_y**2 < 2**2 and self.y > screen_size[1] - 2*self.size:
            self.kill()

    def draw(self, surface: Surface) -> None:
        """
        Uses a static Artist draw function to draw the object to the given surface
        
        Parameters
        ----------
        surface : pygame.Surface
            A surface object to draw the Drawable onto
        """
        Artist.draw(
            surface, 
            self.x, self.y, 
            self.color, self.size, self.shape)
    
    def check_corners(
            self, 
            screen_size: tuple, 
            refl_ort: float = 0.6, refl_par: float = 0.7) -> None:
        """
        Implements inelastic rebound when the projectile hits the screen's edge

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        refl_ort : float
            The coefficient of restitution orthogonal to the surface (default 0.9)
        refl_par : float
            The coefficient of restitution parallel to the surface (default 0.8)
        """

        # If the projectile hits the left edge of the screen
        if self.x < self.size:
            # Make sure we don't go off-screen
            self.x = self.size 

            # Reverse the x velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = -int(self.v_x * refl_ort)
            self.v_y = int(self.v_y * refl_par)

        # If the projectile hits the right edge of the scrteen
        elif self.x > screen_size[0] - self.size:
            # Make sure we don't go off-screen
            self.x = screen_size[0] - self.size

            # Reverse the x velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = -int(self.v_x * refl_ort)
            self.v_y = int(self.v_y * refl_par)

        # If the projectile hits the top of the screen
        if self.y < self.size:
            # Make sure we don't go off-screen
            self.y = self.size

            # Reverse the y velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = int(self.v_x * refl_par)
            self.v_y = -int(self.v_y * refl_ort)
        
        # If the projectile hits the bottom of the screen
        elif self.y > screen_size[1] - self.size:
            # Make sure we don't go off-screen
            self.y = screen_size[1] - self.size

            # Reverse the y velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = int(self.v_x * refl_par)
            self.v_y = -int(self.v_y * refl_ort)

class CircleProjectile(Projectile):
    """A Projectile of shape Circle. Refer to `Projectile`"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            shape = 'c')

class SquareProjectile(Projectile):
    """A Projectile of shape Square. Refer to `Projectile`"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            shape = 's')
        
class TriangleProjectile(Projectile):
    """A Projectile of shape Triangle. Refer to `Projectile`"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            shape = 't')