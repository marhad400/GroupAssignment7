# CS 2520 Group Assignment - Cannon Game - George Matta, Mark Haddad, Ayanna Sanges-Chu
This project refactors the given cannon.py from https://github.com/assamidanov/python_programming_class/tree/main/week13, and expands the game by adding new features. The project is focused on functional and object-oriented programming, where each object of the game inherits from one or several of Drawable, Moveable, and Killable abstract class attributes. Different classes such as the Cannon, Projectiles, Targets, and Bombs are implemented in respective Master classes that are then used in the main Manager to run our desired output. Overall, the game allows the user to control a cannon, fighting against enemy cannons and targets that drop bombs.

# Installation and Running
- Go to desired directory for storing the project (e.g. Desktop: `cd Desktop`)

- Clone the repo: `git clone https://github.com/marhad400/GroupAssignment7.git`

- Install pygame and NumPy:
  - `pip3 install pygame`
  - `pip3 install numpy`

- Run: `python3.10 main.py`

# Project Details
### abstract.py
Defines the three abstract class atributes Drawable, Moveable, and Killable, which define the basis of the functions of the other classes such as draw(), move(), and kill().

### artist.py
Contains a class Artist that defines static methods for various drawing functions, such as draw_score(), draw_cannon, and a draw() function that can specify the specific shape desired. The Artist class allows for easy implementation of the draw() functions in the other Drawable objects, where code is easily reused and more Drawable objects can be created easily.

### color.py
Defines all of the color fields in a class Color, and one static method rand_color() to implement a random color for drawing implementations.

### bombs.py
Defines a Bomb class that inherits Drawable, Moveable and Killable. Bombs are drawn with the Artist class, and have different functions for checking collision with the bottom of the screen or the user, and explodes for either collision. There is also a BombMaster class, which has functions to regulate the usage of bombs within the game, such as create_bomb(), draw_all(), move_all(), and remove_exploded().

### targets.py
Defines a Target class that inherits Drawable and Killable, and MovingTarget that inherits Moveable and Target. All targets are drawn with the Artist in the draw() function, and moving targets check collision for the corners of the screen to bounce off of. Target also implements a BombMaster, as Bombs are being dropped from the various targets in the game. Additionally, there are child classes defined such as StaticSquare, and MovingCircle which inherit traits from the parent Target and MovingTarget classes. These child classes simply specify the shape of the specific target. Finally, there is a TargetMaster to regulate the creation and usage of targets in the game.

### projectiles.py
Defines a Projectile class that inherits Drawable, Killable, and Moveable. The projectiles are drawn with Artist, and also have a check_corners() function to bounce off the screen. There are also additional inherited child classes of Projectile that specify the shape of the different projectiles. Additionally there is a ProjectileMaster to create and mainting the existing Projectiles.

### cannon.py
Defines a Cannon class that inherits Drawable and Killable, MovingCannon that inherits Moveable and Cannon, and ArtificialCannon that inherits MovingCannon. Cannon has constructor atrributes power, angle, and choosing the type of projectile it is shooting using an imported ProjectileMaster. Cannon has various functions to use these attributes such as change_chosen(), gain(), and set_angle(). MovingCannon implements a move() function, and ArtificialCannon implements move() from MovingCannon, and has additional functions to determine its movement and shooting capabilities. Additionally, ArtificialCannon implements an imported TargetMaster used in a determine_target_spawning() function to spawn targets played against the user.

### manager.py
manager.py first has a ScoreTable class, that draws the score property determined by the number of targets destroyed - the number of projectiles used. ScoreTable also draws the game over screen that displays after the user loses enough health to die. The main portion of the file is the Manager class, which initializes and handles all of the objects for the game such as the cannons, projectiles, targets, bombs, and screen. Manager has classes for initializing pygame, updating the display, handling all of the drawing and movement of the objects, collision, and running the main game loop.

### main.py
Imports a Manager object to call the main game loop and run the game.
