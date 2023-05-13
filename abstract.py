class Drawable:
    """A class representing an objects ability to be drawed onto the screen

    Simply includes an empty definition for the draw function, and the necessary
    attributes for a drawable object
    
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
    """

    def __init__(
            self, 
            x: int, y: int, 
            color: tuple, size: int) -> None:
        """Initializes the necessary attributes for a drawable object"""
        self.x, self.y = x, y
        self.color = color
        self.size = size

    def draw() -> None: 
        """An empty definition for a sample draw function"""
        pass

class Moveable:
    """A class representing an objects ability to be moved

    Simply includes an empty definition for the move function, and the necessary
    attributes for a moveable object
    
    Parameters
    ----------
    v_x : int
        The object's velocity in the x direction
    v_y : int 
        The object's velocity in the y direction
    """

    def __init__(
            self, 
            v_x: int, v_y: int) -> None:
        """Initializes the necessary attributes for a moveable object"""
        self.v_x, self.v_y = v_x, v_y
    
    def move() -> None: 
        """An empty definition for a sample move function"""
        pass


class Killable:
    """A class representing an objects ability to be killed

    A bit more involved than the other abstract classes, this class is more 
    concrete in its ability to store and change a health value

    Contains implementations for a heal function (to increase health) and a deal
    function (to decrease health). Also contains a property is_alive to check
    if the object is alive
    
    Parameters
    ----------
    health : int
        An int denoting the object's health. A health value of 1 means the object
        is killed after a single hit.
    """

    def __init__(self, health: int = 1) -> None:
        """Initializes the health to the provided health or a default of 1"""
        self.health = health
    
    def deal(self, damage: int = 1) -> None:
        """
        Deals a certain amount of damage to the object

        Parameters
        ----------
        damage : int
            The amount of damage to deal to the object (default 1)
        """
        self.health -= damage
    
    def heal(self, health: int = 1) -> None:
        """
        Heals a certain amount of health back to the object

        Parameters
        ----------
        health : int
            The amount of health to heal to the object (default 1)
        """
        self.health += health

    def kill(self) -> None:
        """Sets the health to 0"""
        self.health = 0

    @property
    def is_alive(self) -> bool:
        """A property denoting whether or not the object is alive (above 0 health)"""
        return self.health > 0