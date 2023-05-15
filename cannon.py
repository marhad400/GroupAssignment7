import numpy as np
from color import Color
from abstract import Moveable, Drawable, Killable
from artist import Artist

from projectiles import ProjectileMaster
from targets import TargetMaster

from pygame import Surface
import random
import time
import threading

class Cannon(Drawable, Killable):
    """
    A class representing a cannon

    A Cannon can be hit by projectiles, and fires projectiles. It can also be
    hit by bombs.

    A Cannon is a Drawable (meaning it can be drawn to the screen) and is Killable
    (meaning it can take damage and die). This means we need to pass in all the
    attributes necessary for both a Drawable and Killable object.
        
    Attributes
    ----------
    x : int
        The x coordinate of the object
    y : int 
        The y coordinate of the object
    health : int
        An int denoting the object's health
    color : tuple
        A tuple representing the (R, G, B) values of the object's color
    max_pow : int
        The maximum power this cannon can fire (deafault 50)
    min_pow : int
        The minimum power this cannon can fire (default 10)
    pow : int
        The current power of the cannon
    active : bool
        Whether or not the cannon is currently gaining power
    chosen_type : str
        What type of projectile the cannon is currently firing (square, circle, 
        triangle)
    projectile_master : ProjectileMaster
        The cannon's projectile master, in charge of controlling the projectiles 
        fired by this cannon
    """

    def __init__(
            self, 
            x: int, 
            y: int, 
            health: int = 1, 
            color: tuple =None, 
            angle: int= 0, 
            max_pow: int = 50, 
            min_pow: int = 10) -> None:
        """Initializes the cannon's attributes"""
        # Set a random color if one is not provided
        color = color or Color.rand_color()

        # Abstract init
        Drawable.__init__(self, x=x, y=y, color=color, size=1)
        Killable.__init__(self, health=health)

        # Self init
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.pow = min_pow

        # Whether or not the cannon is gaining power
        self.active = False
        
        # The default chosen type of projectile to fire (circle)
        self.chosen_type = 'c'

        # The cannon's projectile master, in charge of controlling the projectiles
        # fired by this cannon
        self.projectile_master = ProjectileMaster()

    def change_chosen(self, chosen_type: str) -> None:
        """
        Changes the currently chosen projectile type
        
        Parameters
        ----------
        chosen_type : str
            The new type of projectile to fire (must start with 's', 't', or 'c')
        """
        if chosen_type[0] not in ['s', 't', 'c']:
            return

        self.chosen_type = chosen_type[0]

    def activate(self) -> None:
        """Activates the gun's charge. Sets active to True"""
        self.active = True

    def gain(self, increment: int = 2) -> None:
        """
        Increases the gun's power by an increment amount
        
        Maxes out at the cannon's max_pow

        Parameters
        ----------
        increment : int
            The amount to increment the power by (default 2)
        """
        if self.active and self.pow < self.max_pow:
            self.pow += increment

    def strike(self, vel: int = None) -> None:
        """
        Fires a projectile based on a velocity. If velocity isn't provided, it 
        defaults to the power of the cannon

        Parameters
        ----------
        vel : int
            The velocity to use for the shot
        """
        vel = vel or self.pow
        
        # Creates a projectile and stores it
        self.projectile_master.create_projectile(
                                                self.x, 
                                                self.y, 
                                                vel, 
                                                self.angle, 
                                                self.chosen_type
                                            )

        # Reset the power and activity  
        self.pow = self.min_pow
        self.active = False
                
    def set_angle(self, target_x: int, target_y: int) -> None:
        """
        Sets the angle of the cannon to a target's position
        
        Parameters
        ----------
        target_x : int
            The x position of the target
        target_y : int
            The y position of the target
        """
        self.angle = np.arctan2(
                                target_y - self.y, 
                                target_x - self.x
                            )

    def draw(self, surface: Surface):
        """
        Draws the cannon by delegating to the Artist draw_cannon method

        Parameters
        ----------
        surface : pygame.Surface:
            The surface to draw the cannon onto
        """
        Artist.draw_cannon(
            surface, self.x, self.y, self.angle, self.pow, self.color
        )

class MovingCannon(Moveable, Cannon):
    """
    A class representing a Moveable Cannon

    A Cannon can be hit by projectiles, and fires projectiles. It can also be
    hit by bombs.

    A Cannon is a Drawable (meaning it can be drawn to the screen) and is Killable
    (meaning it can take damage and die). This means we need to pass in all the
    attributes necessary for both a Drawable and Killable object. In addition,
    this type of cannon can be moved around the screen (making it a Moveable as 
    well).

    MovingCannon simply inherits from the abstract Moveable and the concrete Target        

    Attributes
    ----------
    x : int
        The x coordinate of the object
    y : int 
        The y coordinate of the object
    v_x : int
        The x velocity of the object (default 7)
    v_y : int
        The y velocity of the object  (default 7)
    health : int
        An int denoting the object's health
    color : tuple
        A tuple representing the (R, G, B) values of the object's color
    max_pow : int
        The maximum power this cannon can fire (deafault 50)
    min_pow : int
        The minimum power this cannon can fire (default 10)
    pow : int
        The current power of the cannon
    active : bool
        Whether or not the cannon is currently gaining power
    chosen_type : str
        What type of projectile the cannon is currently firing (square, circle, 
        triangle)
    projectile_master : ProjectileMaster
        The cannon's projectile master, in charge of controlling the projectiles 
        fired by this cannon
    """

    def __init__(
            self, 
            v_x: int = 7, 
            v_y: int = 7,
            *args, **kwargs) -> None:
        """"""
        Moveable.__init__(self, v_x=v_x, v_y=v_y)
        Cannon.__init__(self, *args, **kwargs)

    def move(
            self, 
            screen_size: tuple, 
            move_x: int = 0, 
            move_y: int = 0) -> None:
        """
        Changes the position of the cannon based on its velocity and a multiplier

        The move_x and move_y multipliers should be -1, 0, or 1 depending on if
        the object is moving backwards or not moving at all.

        It can also be used as any other int for a multiplier to the speed

        Parameters
        ----------
        screen_size : tuple
            The size of the screen (used to constrict the movement)
        move_x : int
            The x movement multiplier (default 0)
        move_y : int
            The y movement multiplier (default 0)
        """
        # Move x based on its velocity and constrict it to the screen size
        self.x += move_x * self.v_x
        self.x = max(30, min(self.x, screen_size[0] - 30))

        # Move y based on its velocity and constrict it to the screen size
        self.y += move_y * self.v_y
        self.y = max(30, min(self.y, screen_size[1] - 30))
    
    def move_right(self, screen_size: tuple):
        """
        Delagates to the move function the parameters necessary to move right

        move(1, 0)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, 1, 0)

    def move_left(self, screen_size: tuple):
        """
        Delagates to the move function the parameters necessary to move left

        move(-1, 0)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, -1, 0)
    
    def move_up(self, screen_size: tuple):
        """
        Delagates to the move function the parameters necessary to move up

        move(0, -1)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, 0, -1)
    
    def move_down(self, screen_size: tuple):
        """
        Delagates to the move function the parameters necessary to move down

        move(0, 1)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, 0, 1)

class ArtificialCannon(MovingCannon):
    """
    A class representing an enemy cannon

    Inherits from MovingCannon

    Attributes
    ----------
    Refer to `MovingCannon`
        Changes to default values for v_x and v_y (3) and min_pow (30)
    strike_thread : threading.Thread
        A thread that handles periodic striking   
    """
    def __init__(
            self, 
            v_x: int = 3, 
            v_y: int = 3, 
            min_pow: int = 30, 
            *args, **kwargs) -> None:
        """Initializes the MovingCannon and sets the strike_thread to None"""
        super().__init__(v_x, v_y, min_pow = min_pow, *args, **kwargs)

        self.strike_thread = None

    def determine_move(
            self, 
            user_cannon: Drawable, 
            screen_size: tuple) -> bool:
        """
        Determines which way the cannon should move

        Always tries to follow the user unless it's too close (100 units away)

        Parameters
        ----------
        user_cannon : Drawable
            A Drawable object that is the user cannon
        screen_size : tuple
            The size of the screen. Used to constrict movement

        Returns
        -------
        moved : bool
            Whether or not a movement was made
        """
        # The x and y distances from the user cannon
        d_x = self.x - user_cannon.x
        d_y = self.y - user_cannon.y

        # The linear distance from the cannon
        dist = sum(
                    [
                        (self.x - user_cannon.x)**2, 
                        (self.y - user_cannon.y)**2
                    ]
                )**0.5
        min_dist = self.size + user_cannon.size + 100

        # If we're too close, don't move
        if dist < min_dist:
            return False

        # If we're to the left of the user cannon, move right
        if d_x < 0:
            self.move_right(screen_size)
        # Otherwise, move left
        elif d_x > 0:
            self.move_left(screen_size)
        
        # Similarly, if we're above the cannon, move down
        if d_y < 0:
            self.move_down(screen_size)
        # If we're below it, move up
        elif d_y > 0:
            self.move_up(screen_size)

        return True

    def keep_striking(
            self, 
            delay: float = 0.5, 
            vel_to_shoot: int = 60) -> None:
        """
        Keeps the artificial cannon firing while the strike_thread exists
        
        delay : float
            The delay to wait between shots (default 0.5)
        vel_to_shoot : int
            The power to shoot the shot with (default 60)
        """
        # While the strike_thread exists
        while self.strike_thread:
            # Sleep for delay amount of time, check if the thread exists again
            # (It may have died since the start of checking)
            time.sleep(delay)
            if self.strike_thread:
                # Shoot the shot
                self.strike(vel_to_shoot)

    def start_thread(self) -> None:
        """Starts the strike_thread"""
        if not self.strike_thread:
            self.strike_thread = threading.Thread(
                                                    target=self.keep_striking, 
                                                    daemon=True
                                                )
            self.strike_thread.start()
        
    def end_thread(self):
        """Ends the thread by resetting strike_thread to None"""
        self.strike_thread = None
    
    def determine_target_spawning(
            self, 
            target_master: TargetMaster, 
            score: int, 
            chance: float = 0) -> None:
        """
        Determines whether or not the artificial tank should be dropping
        a target onto the screen

        The artificial tank is always in one of two states: it's either following
        the player and placing targets, or stationary and firing projectiles at
        the user

        We check which state it's in by checking the strike_thread's existance

        Parameters
        ----------
        target_master : TargetMaster
            The controller of all the targets on the screen
        score : int
            The player's score. Used to create the target
        chance : float
            The chances of dropping a target on this tick
        """

        # If the artificial tank is not moving, or we don't get the chance of 
        # dropping a target
        if self.strike_thread or random.random() > chance:
            return
    
        # Uses the target master to create a target
        target_master.create_random_target(
                (0, 0),
                target_master.calculate_target_size(score),
                self.x,
                self.y
            )

