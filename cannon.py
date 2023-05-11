import numpy as np
import pygame as pg
from random import randint, gauss
from color import Color
from targets import TargetMaster
from projectiles import CircleProjectile, SquareProjectile, TriangleProjectile
from abstract import Moveable, Drawable, Killable

pg.init()
pg.font.init()


class Cannon(Moveable, Drawable, Killable):
    '''
    Cannon class. Manages it's renderring, movement and striking.
    '''
    def __init__(self, x, y, v_x: int = 5, v_y: int = 5, angle: int = 0, max_pow: int = 50, min_pow: int = 10, health: int = None, color: tuple = Color.RED):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''

        Drawable.__init__(self, x=x, y=y, color=color, size=1)
        Moveable.__init__(self, v_x=v_x, v_y=v_y)
        Killable.__init__(self, health=health)

        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow

        self.active = False
        self.pow = min_pow
    
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

    def strike(self):
        '''
        Creates ball, according to gun's direction and current charge power.
        '''
        vel = self.pow
        angle = self.angle

        ball = SquareProjectile(self.x, self.y, *[int(vel * np.cos(angle)), int(vel * np.sin(angle))], Color.GREEN, 20, 1)
        self.pow = self.min_pow
        self.active = False
        return ball
        
    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(target_pos[1] - self.y, target_pos[0] - self.x)

    def move(self, move_x: int = 0, move_y: int = 0):
        '''
        Changes vertical position of the gun.
        '''
        if move_x:
            self.x += move_x * self.v_x
            self.x = max(30, min(self.x, Color.SCREEN_SIZE[0] - 30))
            print("move x", self.v_x)
        if move_y:
            self.y += move_y * self.v_y
            self.y = max(30, min(self.y, Color.SCREEN_SIZE[1] - 30))
            print("move y", self.v_y)
        

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

class StaticCannon(Cannon):
    '''
    Cannon class. Manages it's renderring, movement and striking.
    '''
    def __init__(self, x, y, v_x: int = 5, v_y: int = 5, angle: int = 0, max_pow: int = 50, min_pow: int = 10, health: int = None, color: tuple = Color.RED):
        super().__init__(
            x = x, y = y, 
            v_x = v_x, v_y = v_y, 
            angle = angle, 
            max_pow = max_pow, min_pow = min_pow, 
            health = health, color = color
        )

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
        self.balls = []
        self.gun = Cannon(30, Color.SCREEN_SIZE[1]//2)
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
        
        self.move()
        self.collide()
        self.draw(screen)

        if len(self.target_master.target_list) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''
        done = False
        
        keys_pressed = pg.key.get_pressed()
        
        move_x = -1 if keys_pressed[pg.K_LEFT] else 1 if keys_pressed[pg.K_RIGHT] else 0
        move_y = -1 if keys_pressed[pg.K_UP] else 1 if keys_pressed[pg.K_DOWN] else 0

        self.gun.move(move_x, move_y)

        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        for ball in self.balls:
            ball.draw(screen)
        self.target_master.draw_all(screen)
        self.gun.draw(screen)
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
        '''
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move(grav=2)
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        self.target_master.move_all()
        self.gun.gain()

    def collide(self):
        '''
        Checks whether balls bump into targets, sets balls' alive trigger.
        '''
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.balls):
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
