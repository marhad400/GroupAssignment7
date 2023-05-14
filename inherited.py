from abstract import Drawable, Killable, Moveable
from color import Color
from artist import Artist

import random
from pygame import Surface

class Target(Drawable, Killable):
    """A class representing a target

    A target can be hit by projectiles, and can be a circle, triangle, or square.
    Only projectiles of the same shape as the target can deal damage.

    A Target is a Drawable (meaning it can be drawn to the screen) and is Killable
    (meaning it can take damage and die). This means we need to pass in all the
    attributes necessary for both a Drawable and Killable object, and an attribute
    for the shape.
    
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
            color: tuple = None, 
            size: int = 5, 
            health: int = 1, 
            shape: str = 'c') -> None:
        """
        Intiailizes the necessary values for a Drawable, Killable, object using the
        init functions of both abstract classes, respectively

        While the default value for color, size, health, and shape looks to be None,
        the function defaults those to a random color, 5, 1, and 'c' for circle.
        This is due to behavior in Python with passing attributes through super
        functions.
        """
        color = color or Color.rand_color()

        # Parent class initialization
        Drawable.__init__(self, x=x, y=y, color=color, size=size)
        Killable.__init__(self, health=health)
        # Shape initialization
        self.shape = shape
    
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

    def __str__(self) -> str:
        """Returns a string representation of the object"""

        return f"Static Target of Shape({self.shape}), " \
                f"Pos({self.x}, {self.y}), " \
                f"Color({self.color}), Size({self.size}), Health({self.health})"
            
    def __repr__(self) -> str:
        """Delegates to __str__"""
        return self.__str__()

class MovingTarget(Moveable, Target):
    """A class representing a moving target

    A target can be hit by projectiles, and can be a circle, triangle, or square.
    Only projectiles of the same shape as the target can deal damage.

    A Target is a Drawable (meaning it can be drawn to the screen) and is Killable
    (meaning it can take damage and die). This means we need to pass in all the
    attributes necessary for both a Drawable and Killable object, and an attribute
    for the shape. In addition, this type of target can be moved around the screen
    (making it a Moveable as well).

    MovingTarget simply inherits from the abstract Moveable and the concrete Target
        
    Parameters
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
            v_x: int = None, 
            v_y: int = None, 
            color: tuple = None, 
            size: int = 30, 
            health: int = 1, 
            shape: str = None) -> None:
        """
        Intiailizes the necessary values for a Moveable, Target, object using
        both classes' init functions 

        While the default value for velocities, color, size, health, and shape 
        looks to be None, the function defaults those to random numbers
        between -2 and 2, a random color, 30, 1, and 'c' for circle.
        This is due to behavior in Python with passing attributes through super
        functions.
        """
        v_x = v_x or random.randint(-2, 2)
        v_y = v_y or random.randint(-2, 2)
        color = color or Color.rand_color()

        # Parent class initialization
        Moveable.__init__(self, v_x, v_y)
        Target.__init__(self, x, y, color, size, health, shape)
    
    def move(self, screen_size):
        """Changes the x and y position of the object depending on the velocities"""
        self.x += self.v_x
        self.y += self.v_y

        self.check_corners(screen_size)
    
    def check_corners(self, screen_size) -> None:
        """
        Implements inelastic rebound when the projectile hits the screen's edge

        Parameters
        ----------
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
            self.v_x = -int(self.v_x)
            self.v_y = int(self.v_y)

        # If the projectile hits the right edge of the scrteen
        elif self.x > screen_size[0] - self.size:
            # Make sure we don't go off-screen
            self.x = screen_size[0] - self.size

            # Reverse the x velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = -int(self.v_x)
            self.v_y = int(self.v_y)

        # If the projectile hits the top of the screen
        if self.y < self.size:
            # Make sure we don't go off-screen
            self.y = self.size

            # Reverse the y velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = int(self.v_x)
            self.v_y = -int(self.v_y)
        
        # If the projectile hits the bottom of the screen
        elif self.y > screen_size[1] - self.size:
            # Make sure we don't go off-screen
            self.y = screen_size[1] - self.size

            # Reverse the y velocity and calculate the new velocities (decreased)
            # based on the reflection parameters
            self.v_x = int(self.v_x)
            self.v_y = -int(self.v_y)
    
    def __str__(self):
        """Returns a string representation of the object"""

        return f"Moving Target of Shape({self.shape}), " \
                f"Pos({self.x}, {self.y}), " \
                f"Color({self.color}), Size({self.size}), Health({self.health}), " \
                f"Speed({self.v_x}, {self.v_y})"
    
    def __repr__(self):
        """Returns a string representation of the object"""
        return self.__str__()

class Projectile(Drawable, Killable, Moveable):
    """A class representing a projectile

    A projectile (which can be one of a square, circle, or triangle) can hit 
    a target of the same shape, or the cannon.

    A Projectile is Drawable, Killable, and Moveable, meaning it needs
    all the attributes for all of those abstract classes.
        
    Parameters
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
            screen_size, time: int = 1, grav: int = 0) -> None:
        """
        Moves the projectile based on its velocity and the effect of gravity

        Parameters
        ----------
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
            screen_size, refl_ort: float = 0.8, refl_par: float = 0.9) -> None:
        """
        Implements inelastic rebound when the projectile hits the screen's edge

        Parameters
        ----------
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

class Bomb(Drawable, Killable, Moveable):
    def __init__(
            self, 
            x: int, 
            y: int, 
            v_y: int = None,
            v_x: int = 0,  
            size: int = 40, 
            health: int = 1,
            color: int = None, 
            shape: int = 'c') -> None:
        
        color = color or Color.RED

        # Parent class initialization
        Drawable.__init__(self, x, y, color=color, size=size)
        Killable.__init__(self, health=health)
        Moveable.__init__(self, v_y=v_y, v_x=v_x)
        # Shape initialization
        self.shape = shape
    
    def move(self, time: int = 1, grav: int = 0) -> None:
        
        #Add gravity
        self.v_y += grav

        # Change y-position based on gravity
        self.y += time * self.v_y

    def draw(self, surface: Surface) -> None:

        Artist.draw(
            surface,
            self.x, self.y,
            self.color, self.size, self.shape
        )
    
    def check_bottom(self, screen_size):
        
        #If the projectile reaches the bottom of the screen
        at_bottom = False
        if self.y < screen_size[1] -self.size:
            at_bottom = True

        return at_bottom
    
    def explode(self, screen_size):
        if self.check_bottom(screen_size):
            self.kill()