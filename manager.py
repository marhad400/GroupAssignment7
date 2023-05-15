from cannon import MovingCannon, ArtificialCannon
from targets import TargetMaster
from color import Color
from artist import Artist

import threading
import pygame
import time
import random

class ScoreTable:
    """
    A class that keeps track of the score the user manages to get
    
    The score is determined by the difference of targets destroyed
    and projectiles used (which are both maintained by this class as well).

    This class also handles the font we're using to render text

    Attributes
    ----------
    targets_destroyed : int
        The number of targets destroyed
    projectiles_used : int
        The number of projectiles used
    font_name : str
        The name of the font we're using (default dejavusansmono)
    font_size : int 
        The font size (default 25)
    font : pygame.font.Font
        The font we're using
    score: int
        The number of targets destroyed
    
    """
    def __init__(
            self, 
            targets_destroyed: int = 0, 
            projectiles_used: int = 0, 
            font_name: str = "dejavusansmono", 
            font_size: int = 25):
        """Initializes the score table"""
        self.targets_destroyed = targets_destroyed
        self.projectiles_used = projectiles_used
        self.font = pygame.font.SysFont(font_name, font_size)
    
    @property
    def score(self) -> int:
        """A property that calculates and returns the score"""
        return self.targets_destroyed - self.projectiles_used

    def draw(
            self, 
            surface: pygame.Surface, 
            chosen_type: str = None, 
            health : int = None) -> None:
        """
        Draws the score table by delegating to the Artist draw_score method

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the table onto
        chosen_type : str
            The currently chosen projectile type
        health : int
            The user's health
        """
        Artist.draw_score(
            surface, 
            self.font, 
            self.targets_destroyed, 
            self.projectiles_used, 
            self.score,
            chosen_type,
            health,
            Color.RED, 
            Color.WHITE
            )
    
    def draw_game_over_screen(
                        self,
                        surface: pygame.Surface,
                        game_over_text: str) -> None:
        """
        Draws the game over screen
        
        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the game over screen onto
        """
        Artist.draw_death_screen(
            surface, 
            self.font, 
            game_over_text,
            self.score,
            Color.RED
        )

class Manager:
    """
    The main Manager class that runs the entire project

    Keeps track of the screen, pygame initialization, the game loop, and every
    object used

    Parameters
    ----------
    num_targets : int
        The initial number of targets to spawn (default 10)
    num_cannons : int
        The initial number of artifical cannons to spawn (default 3)
    screen : pygame.Surface
        The screen surface we draw everything onto 
    clock : pygame.Clock
        The clock (keeps track of in-game ticks)
    refresh_rate : int
        The refresh rate of the game (default 15)
    user_cannon : MovingCannon
        The player object
    artficial_cannons : list[ArtificialCannon]
        A list of the artificial enemy cannons
    target_master : TargetMaster
        The controller of all the targets on the screen
    bomb_spawning_thread : threading.Thread
        A thread that handles periodic bomb spawning for all targets
    """
    def __init__(
            self, 
            num_targets: int = 10, 
            num_cannons: int = 3) -> None:
        """Initializes the Manager"""
        self.screen_size = (800, 600)
        self.init_pygame()
        self.init_clock()
        self.done = False

        self.num_cannons = num_cannons
        self.init_cannons()

        self.score_t = ScoreTable()
        self.num_targets = num_targets
        self.bomb_spawning_thread = None
        self.start_bomb_thread()
        
        self.update_display()

    def init_pygame(self) -> None:
        """Initalizes the Pygame module and the screen"""
        pygame.display.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("The Gun of Khiryanov II")

    def update_display(self) -> None:
        """Updates the Pygame screen by calling display.flip()"""
        pygame.display.flip()

    def init_clock(self) -> None:
        """Initializes the Pygame clock and refresh rate"""
        self.clock = pygame.time.Clock()
        self.refresh_rate = 15

    def init_cannons(self) -> None:
        """Intializes the user cannon, artificial cannons, and target_master"""
        
        # Create the user cannon
        self.user_cannon = MovingCannon(
            x = 30, 
            y = self.screen_size[1]//2,
            color = Color.LIGHT_BLUE
        )

        # Initializes an artifical cannon for each cannon we should have
        self.artificial_cannons: list[ArtificialCannon] = []
        for _ in range(self.num_cannons):
            self.artificial_cannons.append(ArtificialCannon(
            x = random.randint(self.screen_size[0]//2, self.screen_size[0] - 30), 
            y = random.randint(0, self.screen_size[1]),
            v_x = random.randint(2, 5),
            v_y = random.randint(2, 5),
            color = Color.RED
        ))

        self.target_master = TargetMaster()

    def process_states(self) -> None:
        """Processes the entire game - an aspect of the main game loop"""
        # Handle any inputs by the player
        self.handle_events()
        
        # Set the user and artificial cannon angles
        self.handle_angles()

        # Handle movement
        self.handle_cannon_movement() # cannon 
        self.handle_target_movement() # targets
        self.handle_projectile_movement() # projectiles
        self.handle_bomb_movement() # bombs
        
        # Handle collisions
        self.handle_collisions()

        # Handle dead objects
        self.handle_exploded_bombs() # bombs
        self.handle_dead_projectiles() # projectiles

        # Handles new sets of target spawns
        self.handle_new_missions()

        # Draw everything to the screen
        self.handle_drawing()
        self.update_display()
    
    def handle_angles(self) -> None:
        """
        Handles the angle of the user and artificial cannon
        
        Sets the user cannon's angle to the mouse position, and the artificial
        cannon angle to the user position
        """

        # Get mouse position and set angle
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            self.user_cannon.set_angle(*mouse_pos)
        
        # Set each artificial cannon's angle to the user
        for artificial_cannon in self.artificial_cannons:
            artificial_cannon.set_angle(self.user_cannon.x, self.user_cannon.y)

    def handle_cannon_movement(self) -> None:
        """Handle artificial and user cannon movement and type switching"""
        
        # Which key corresponds to what movement
        key_to_move = {
            pygame.K_LEFT: self.user_cannon.move_left,
            pygame.K_RIGHT: self.user_cannon.move_right,
            pygame.K_UP: self.user_cannon.move_up,
            pygame.K_DOWN: self.user_cannon.move_down,
            
            pygame.K_a: self.user_cannon.move_left,
            pygame.K_d: self.user_cannon.move_right,
            pygame.K_w: self.user_cannon.move_up,
            pygame.K_s: self.user_cannon.move_down
        }

        # Which key corresponds to what type of projectile
        type_switcher = {
            pygame.K_1: 's',
            pygame.K_2: 'c',
            pygame.K_3: 't'
        }

        # Move depending on the move key
        keys_pressed = pygame.key.get_pressed()
        for key, move_func in key_to_move.items():
            if keys_pressed[key]:
                move_func(self.screen_size)
        
        # Switch depending on the switch key
        for key, chosen_type in type_switcher.items():
            if keys_pressed[key]:
                self.user_cannon.change_chosen(chosen_type)
        
        # Check if the user cannon should be gaining power
        self.user_cannon.gain()

        # Starts or ends the thread depending on if the artificial cannon
        # is within range (or spawn targets if it isn't)
        for artificial_cannon in self.artificial_cannons:
            
            if artificial_cannon.determine_move(
                                                self.user_cannon, 
                                                self.screen_size
                                                ):
                artificial_cannon.end_thread()
            
            else:
                artificial_cannon.start_thread()
        
            artificial_cannon.determine_target_spawning(
                self.target_master, self.score_t.score, 0.01
                )

    def handle_target_movement(self) -> None:
        """Handles the movement of all the targets"""
        self.target_master.move_all(self.screen_size)

    def handle_projectile_movement(self) -> None:
        """Handles the movement of all the projectiles"""
        self.user_cannon.projectile_master.move_all(self.screen_size)
        
        for artificial_cannon in self.artificial_cannons:
            artificial_cannon.projectile_master.move_all(self.screen_size)

    def handle_dead_projectiles(self) -> None:
        """Removes dead projectiles from the screen"""
        self.user_cannon.projectile_master.remove_dead()
        for artificial_cannon in self.artificial_cannons:
            artificial_cannon.projectile_master.remove_dead()

    def handle_bomb_movement(self) -> None:
        """Handles the movement of all the bombs"""
        for target in self.target_master.target_list:
            target.bomb_master.move_all()

    def handle_exploded_bombs(self) -> None:
        """Removes dead bombs from the screen"""
        for target in self.target_master.target_list:
            target.bomb_master.remove_exploded(
                                                self.screen_size[1], 
                                                self.user_cannon
                                            )

    def handle_collisions(self) -> None:
        """Handles target and user collisions by delagating to the respective function"""
        self.handle_target_collisions()
        self.handle_user_collision()
        self.handle_artificial_collision()
    
    def handle_target_collisions(self) -> None:
        """
        Handles target collisions by checking if any projectile collided
        with any target. The objects must agree on shape type
        """
        for projectile in self.user_cannon.projectile_master.projectile_list:
            for target in self.target_master.target_list:
                
                if target.check_collision(projectile):
                    
                    if target.shape == projectile.shape:
                        self.target_master.target_list.remove(target)
                        self.score_t.targets_destroyed += 1
                
    def handle_user_collision(self) -> None:
        """
        Handles user collisions by checking if any artificial projectile
        collided with the user
        """
        for artificial_cannon in self.artificial_cannons:
            for projectile in artificial_cannon.projectile_master.projectile_list:
                if self.user_cannon.check_collision(projectile):
                    self.user_cannon.deal()
                    artificial_cannon.projectile_master.projectile_list.remove(projectile)
    
    def handle_artificial_collision(self) -> None:
        """
        Handles artificial cannon collisions by checking if any user
        projectiles collided with the artificial cannon
        """
        for artificial_cannon in self.artificial_cannons:
            for projectile in self.user_cannon.projectile_master.projectile_list:
                
                if artificial_cannon.check_collision(projectile):
                    artificial_cannon.deal()
                    
                    if not artificial_cannon.is_alive:
                        self.artificial_cannons.remove(artificial_cannon)    
                    
                    self.user_cannon.projectile_master.projectile_list.remove(projectile)


    def handle_drawing(self) -> None:
        """Handles drawing all the objects"""
        # Fills the background color
        self.screen.fill(Color.BLACK)
        self.draw_projectiles()
        self.draw_targets()
        self.draw_cannons()
        self.draw_bombs()
        self.draw_score()

    def draw_projectiles(self) -> None:
        """Draws every projectile"""
        self.user_cannon.projectile_master.draw_all(self.screen)
        for artificial_cannon in self.artificial_cannons:
            artificial_cannon.projectile_master.draw_all(self.screen)

    def draw_targets(self) -> None:
        """Draws every target""" 
        self.target_master.draw_all(self.screen)

    def draw_cannons(self) -> None:
        """Draws every cannon"""
        self.user_cannon.draw(self.screen)
        for artificial_cannon in self.artificial_cannons:
            artificial_cannon.draw(self.screen)

    def draw_bombs(self) -> None:
        """Draws every bomb"""
        for target in self.target_master.target_list:
            target.bomb_master.draw_all(self.screen)

    def draw_score(self) -> None:
        """Draws the score table"""
        self.score_t.draw(
                        self.screen, 
                        self.user_cannon.chosen_type, 
                        self.user_cannon.health
                    )

    def handle_events(self) -> None:
        """Handles Pygame events"""
        for event in pygame.event.get():

            # If the user quits
            if event.type == pygame.QUIT:
                self.done = True

            # If they press the left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.user_cannon.activate()

            # If they stop pressing the left mouse button
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.user_cannon.strike()
                    self.score_t.projectiles_used += 1

    def handle_new_missions(self) -> None:
        """Creates a new set of targets if the user killed all of them"""
        if not self.target_master.target_list:
            if not self.user_cannon.projectile_master.projectile_list:
                self.create_mission()

    def create_mission(self) -> None:
        """Creates a num_targets amount of random targets"""
        for _ in range(self.num_targets):
            self.target_master.create_random_target(
                self.screen_size,
                self.target_master.calculate_target_size(self.score_t.score),
            )
    
    def start_bomb_thread(self) -> None:
        """Starts the bomb_spawning_thread"""
        if not self.bomb_spawning_thread:
            self.bomb_spawning_thread = threading.Thread(
                target=self.spawn_bombs, daemon=True
                )
            self.bomb_spawning_thread.start()
    
    def spawn_bombs(self, delay = 0.5, stagger = 0.1, chance = 0.8):
        """
        Spawn bombs depending on the delay, stagger, and chance
        
        Parameters
        ----------
        delay : float
            The delay to wait between bomb dropping checks (default 0.5)
        stagger : float
            The delay to wait between each target dropping their bombs
            This is to prevent all the bombs from getting dropped at the
            same time (default 0.1)
        chance : float
            The decimal chance of a target dropping a bomb on a given tick
        """
        # While the bomb_spawning_thread is active
        while self.bomb_spawning_thread:

            # Wait for the delay
            time.sleep(delay)

            # If it is still active
            if self.bomb_spawning_thread:
                # Randomize which target we're dropping bombs from
                random.shuffle(self.target_master.target_list)
                                
                for target in self.target_master.target_list:
                    # Stagger bomb drops so they don't all come out at the 
                    # same time
                    time.sleep(stagger)
                    
                    # Create a bomb with the given chance
                    target.bomb_master.create_bomb(
                        target.x, target.y + target.size, 1, chance
                    )

    def end_bomb_thread(self):
        """Ends the bomb_spawning_thread by resetting it to None"""
        self.bomb_spawning_thread = None

    def game_loop(self):
        """Keep playing until the user ends the game"""
        while not self.done:
            self.clock.tick(self.refresh_rate)

            self.process_states()
            self.check_game_over()
        
        self.game_over_loop()

    def check_game_over(self):
        if not self.user_cannon.is_alive or self.check_ac_death():
            self.done = True

    def check_ac_death(self):
        return all([not ac.is_alive for ac in self.artificial_cannons])

    def game_over_loop(self):
        show_game_over = True
        while show_game_over:

            if not self.user_cannon.is_alive:
                self.score_t.draw_game_over_screen(self.screen, "You Died!")

            if self.check_ac_death():
                self.score_t.draw_game_over_screen(self.screen, "You Won!")

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    show_game_over = False

            self.update_display()
        
        
        pygame.quit()


