import numpy as np
import pygame as pg
from random import randint, gauss
from color import Color
from targets import TargetMaster
from projectiles import CircleProjectile, SquareProjectile, TriangleProjectile
from abstract import Moveable, Drawable, Killable

import time
import threading

pg.init()
pg.font.init()

class Cannon(Drawable, Killable):

    def __init__(self, x, y, health=1, color=None, angle=0, max_pow=50, min_pow=10):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        color = color or Color.rand_color()

        Drawable.__init__(self, x=x, y=y, color=color, size=1)
        Killable.__init__(self, health=health)

        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow

        self.active = False
        self.pow = min_pow

        self.fired_projectiles = []

    def activate(self):
        '''
        Activates gun's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current gun charge power.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self, vel = None):
        '''
        Creates ball, according to gun's direction and current charge power.
        '''
        vel = vel or self.pow
        angle = self.angle
        
        projectile = SquareProjectile(self.x, self.y, int(vel * np.cos(angle)), int(vel * np.sin(angle)), Color.GREEN, 20, 1)
        self.pow = self.min_pow
        self.active = False
        
        self.fired_projectiles.append(projectile)
        
    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(target_pos[1] - self.y, target_pos[0] - self.x)

    def remove_dead(self):
        for projectile in self.fired_projectiles:
            if not projectile.is_alive:
                self.fired_projectiles.remove(projectile)    

    def draw(self, screen):
        '''
        Draws the gun on the screen.
        '''
        gun_shape = []
        vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)), int(5*np.sin(self.angle - np.pi/2))])
        vec_2 = np.array([int(self.pow*np.cos(self.angle)), int(self.pow*np.sin(self.angle))])
        gun_pos = np.array([self.x, self.y])
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        pg.draw.polygon(screen, self.color, gun_shape)

class MovingCannon(Moveable, Cannon):
    
    def __init__(self, v_x=20, v_y=6, *args, **kwargs):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''

        Moveable.__init__(self, v_x=v_x, v_y=v_y)
        Cannon.__init__(self, *args, **kwargs)

    def move(self, move_x: int = 0, move_y: int = 0):
        '''
        Changes vertical position of the gun.
        '''
        self.x += move_x * self.v_x
        self.x = max(30, min(self.x, Color.SCREEN_SIZE[0] - 30))
        
        self.y += move_y * self.v_y
        self.y = max(30, min(self.y, Color.SCREEN_SIZE[1] - 30))
    
    def move_right(self):
        self.move(1, 0)

    def move_left(self):
        self.move(-1, 0)
    
    def move_up(self):
        self.move(0, -1)
    
    def move_down(self):
        self.move(0, 1)

class ArtificialCannon(MovingCannon):
    '''
    Tank class. Manages its renderring, movement, and striking. 
    '''
    def __init__(self, v_x = 3, v_y = 3, min_pow = 30, *args, **kwargs):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        super().__init__(v_x, v_y, min_pow = min_pow, *args, **kwargs)

        self.strike_thread = None

    def determine_move(self, user_cannon):
        d_x = self.x - user_cannon.x
        d_y = self.y - user_cannon.y

        dist = sum(
                    [
                        (self.x - user_cannon.x)**2, 
                        (self.y - user_cannon.y)**2
                    ]
                )**0.5
        min_dist = self.size + user_cannon.size + 100
        
        if dist < min_dist:
            return False

        if d_x < 0:
            self.move_right()
        elif d_x > 0:
            self.move_left()
        
        if d_y < 0:
            self.move_down()
        elif d_y > 0:
            self.move_up()

        return True

    def keep_striking(self):
        while self.strike_thread:
            time.sleep(1)
            if self.strike_thread:
                self.strike(vel=60)

    def start_thread(self):
        if not self.strike_thread:
            self.strike_thread = threading.Thread(target=self.keep_striking, daemon=True)
            self.strike_thread.start()
        
    def end_thread(self):
        self.strike_thread = None

class ScoreTable:
    '''
    Score table class.
    '''
    def __init__(self, t_destr=0, b_used=0):
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pg.font.SysFont("dejavusansmono", 25)

    def score(self):
        '''
        Score calculation method.
        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        score_surf = []
        score_surf.append(self.font.render("Destroyed: {}".format(self.t_destr), True, Color.WHITE))
        score_surf.append(self.font.render("Balls used: {}".format(self.b_used), True, Color.WHITE))
        score_surf.append(self.font.render("Total: {}".format(self.score()), True, Color.RED))
        for i in range(3):
            screen.blit(score_surf[i], [10, 10 + 30*i])


class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.
    '''
    def __init__(self, n_targets=5):
        self.gun = MovingCannon(x=30, y=Color.SCREEN_SIZE[1]//2, color=Color.LIGHT_BLUE)
        self.artificial_gun = ArtificialCannon(x=Color.SCREEN_SIZE[0] - 30, y=Color.SCREEN_SIZE[1]//2, color=Color.RED)
        self.target_master = TargetMaster()
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def calculate_size(self):
        score = max(0, self.score_t.score())
        upper_bound = max(1, 30 - 2*score)
        lower_bound = 30 - score

        return randint(upper_bound, lower_bound)

    def new_mission(self):
        '''
        Adds new targets.
        '''
        for _ in range(self.n_targets):
            
            self.target_master.create_random_target(
                Color.SCREEN_SIZE,
                self.calculate_size(),
                True
            )
            self.target_master.create_random_target(
                Color.SCREEN_SIZE,
                self.calculate_size(),
                True
            )


    def process(self, events, screen):
        '''
        Runs all necessary method for each iteration. Adds new targets, if previous are destroyed.
        '''
        done = self.handle_events(events)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        user_pos = self.gun.x, self.gun.y
        self.artificial_gun.set_angle(user_pos)
        
        self.move()
        self.collide()
        self.draw(screen)

        if not self.target_master.target_list and not self.gun.fired_projectiles:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''
        done = False
        
        
        key_to_move = {
            pg.K_LEFT: self.gun.move_left,
            pg.K_RIGHT: self.gun.move_right,
            pg.K_UP: self.gun.move_up,
            pg.K_DOWN: self.gun.move_down,
            
            pg.K_a: self.gun.move_left,
            pg.K_d: self.gun.move_right,
            pg.K_w: self.gun.move_up,
            pg.K_s: self.gun.move_down
        }

        keys_pressed = pg.key.get_pressed()
        for key, move_func in key_to_move.items():
            if keys_pressed[key]:
                move_func()

        if self.artificial_gun.determine_move(self.gun):
            self.artificial_gun.end_thread()
        else:
            self.artificial_gun.start_thread()

        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.gun.strike()
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        for ball in self.gun.fired_projectiles + self.artificial_gun.fired_projectiles:
            ball.draw(screen)
        self.target_master.draw_all(screen)
        self.gun.draw(screen)
        self.artificial_gun.draw(screen)
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
        '''
        for ball in self.gun.fired_projectiles + self.artificial_gun.fired_projectiles:
            ball.move(grav=2)
        
        self.gun.remove_dead()
        self.artificial_gun.remove_dead()

        self.target_master.move_all()
        self.gun.gain()

    def collide(self):
        '''
        Checks whether balls bump into targets, sets balls' alive trigger.
        '''
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.gun.fired_projectiles):
            for j, target in enumerate(self.target_master.target_list):
                if target.check_collision(ball):
                    collisions.append([i, j])
                    targets_c.append(j)
        targets_c.sort()
        for j in reversed(targets_c):
            self.score_t.t_destr += 1
            self.target_master.target_list.pop(j)


screen = pg.display.set_mode(Color.SCREEN_SIZE)
pg.display.set_caption("The gun of Khiryanov")

done = False
clock = pg.time.Clock()

mgr = Manager(n_targets=3)

while not done:
    clock.tick(15)
    screen.fill(Color.BLACK)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()

pg.quit()
