from abstract import Drawable, Killable, Moveable
from color import Color
from artist import Artist
from bombs import BombMaster

from pygame import Surface
import random

class TargetMaster:

    def __init__(self):
        self.target_list: list[Target] = []

    def create_random_target(self, screen_size, target_size, x = None, y = None, is_moving: bool = None):
        is_moving = is_moving if is_moving is not None else bool(random.randint(0, 1))

        moving_target_type = [
            MovingSquare, 
            MovingTriangle, 
            MovingCircle 
        ]
        static_target_type = [
            StaticSquare,
            StaticTriangle,
            StaticCircle
        ]

        chosen_type: Drawable = None
        params: dict = {
            'x': x or random.randint(target_size, screen_size[0] - target_size),
            'y': y or random.randint(target_size, screen_size[1] - target_size),
            'size': target_size
        }
        if is_moving:
            chosen_type = random.choice(moving_target_type)
        else:
            chosen_type = random.choice(static_target_type)
        
        created_target = chosen_type(**params)

        self.target_list.append(created_target)

    def calculate_target_size(self, score):
        score = max(0, score)

        weight = 1/(score + 1)

        return int(random.uniform(10, min(30, 30 + weight * 20)))

    def draw_all(self, surface):
        [target.draw(surface) for target in self.target_list]
    
    def move_all(self, screen_size):
        [target.move(screen_size) for target in self.target_list if isinstance(target, MovingTarget)]

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

        self.bomb_master = BombMaster()
    
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

class MovingSquare(MovingTarget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')

class MovingTriangle(MovingTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')

class MovingCircle(MovingTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')

class StaticSquare(Target):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')

class StaticTriangle(Target):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')

class StaticCircle(Target):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs, 
            shape = 'c')