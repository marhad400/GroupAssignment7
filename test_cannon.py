import unittest
from cannon import Cannon, MovingCannon, ArtificialCannon
from color import Color
from projectiles import ProjectileMaster
from artist import Artist
from abstract import Moveable, Drawable, Killable
from targets import TargetMaster


class TestCannon(unittest.TestCase):

    def setUp(self):
        self.test_cannon = Cannon(x = 100, y = 100, color = Color.RED)
        self.projectile_master = ProjectileMaster()
        self.test_moving_cannon = Moveable(v_x = 7, v_y = 7)

    def test_init(self):
        self.test_cannon = Cannon(x = 100, y = 100, color = Color.RED)

        self.assertEqual(self.test_cannon.x, 100)
        self.assertNotEqual(self.test_cannon.x, -1)
        self.assertNotEqual(self.test_cannon.x, 900)
        self.assertEqual(self.test_cannon.y, 100)
        self.assertNotEqual(self.test_cannon.y, -100)
        self.assertNotEqual(self.test_cannon.y, 900)
        self.assertEqual(self.test_cannon.health, 15)
        self.assertNotEqual(self.test_cannon.health, -1)
        self.assertNotEqual(self.test_cannon.health, -100)
        self.assertEqual(self.test_cannon.color, Color.RED)
        self.assertNotEqual(self.test_cannon.color, Color.LIGHT_BLUE)
        self.assertEqual(self.test_cannon.angle, 0)
        self.assertNotEqual(self.test_cannon.angle, -180)
        self.assertNotEqual(self.test_cannon.angle, 360)
        self.assertEqual(self.test_cannon.max_pow, 50)
        self.assertNotEqual(self.test_cannon.max_pow, 100)
        self.assertNotEqual(self.test_cannon.max_pow, -50)
        self.assertEqual(self.test_cannon.min_pow, 10)
        self.assertNotEqual(self.test_cannon.min_pow, 50)
        self.assertNotEqual(self.test_cannon.min_pow, -100)
        self.assertNotEqual(self.test_cannon.min_pow, 0)
        self.assertEqual(self.test_cannon.pow, 10)
        self.assertNotEqual(self.test_cannon.pow, -10)
        self.assertNotEqual(self.test_cannon.pow, 0)
        self.assertFalse(self.test_cannon.active, False)
        self.assertEqual(self.test_cannon.chosen_type, 'c')
        self.assertIsInstance(self.test_cannon.projectile_master, ProjectileMaster)

    def test_change_chosen(self):
        # test when change_chosen is set to 's'
        self.test_cannon.change_chosen('s') 
        self.assertEqual(self.test_cannon.chosen_type, 's')
        self.assertNotEqual(self.test_cannon.change_chosen, 'z')
        # test when change_chosen is set to 'a'
        self.assertIsNone(self.test_cannon.change_chosen('a'))
        #test when change_chosen is set to default
        self.test_cannon.change_chosen('c')
        self.assertEqual(self.test_cannon.chosen_type, 'c')

    def test_activate(self):
        self.assertFalse(self.test_cannon.active)
        self.test_cannon.activate()
        self.assertTrue(self.test_cannon.active)

    def test_gain(self):
        self.test_cannon.gain()
        self.assertEqual(self.test_cannon.pow, 10)
        self.test_cannon.activate()
        self.test_cannon.gain()
        self.assertEqual(self.test_cannon.pow, 12)
        self.test_cannon.gain(50)
        self.assertEqual(self.test_cannon.pow, 62)
        self.test_cannon.gain(8)
        self.assertNotEqual(self.test_cannon.pow, 70)
        self.assertEqual(self.test_cannon.pow, 62)

    def test_strike(self):
        #self.assertIsInstance(self.projectile_master, Cannon(x = int, y = int))
        #tests that strike changes activate to false
        self.test_cannon.activate()
        self.assertTrue(self.test_cannon.active)
        self.test_cannon.strike()
        self.assertFalse(self.test_cannon.active)

        self.test_cannon.activate()
        self.test_cannon.gain()
        self.assertEqual(self.test_cannon.pow, 12)
        self.test_cannon.strike()
        self.assertEqual(self.test_cannon.pow, 10)

        self.assertEqual(self.test_cannon.pow, 10)
        self.assertFalse(self.test_cannon.active)
        self.assertNotEqual(self.test_cannon.pow, 15)
        self.test_cannon.strike(vel = 15)
        self.assertNotEqual(self.test_cannon.pow, 15)


    def test_set_angle(self):
        self.assertEqual(self.test_cannon.angle, 0)
        self.test_cannon.set_angle(200, 200)
        self.assertEqual(self.test_cannon.angle, 0.7853981633974483)
        self.assertNotEqual(self.test_cannon.angle, -0.7853981633974483)

    # def test_draw(self):
    #     self.test_cannon.draw(surface = 100)
    #     self.test_cannon.draw()
    #     self.assertEqual(self.test_cannon.draw())

class TestMovingCannon(unittest.TestCase):
    def test_init(self):
        self.test_moving_cannon = MovingCannon(x = 100, y = 100, v_x = 7, v_y = 7)

        self.assertEqual(self.test_moving_cannon.v_x, 7)
        self.assertNotEqual(self.test_moving_cannon.v_x, -1)
        self.assertNotEqual(self.test_moving_cannon.v_x, 0)
        self.assertEqual(self.test_moving_cannon.v_y, 7)
        self.assertNotEqual(self.test_moving_cannon.v_y, -1)
        self.assertNotEqual(self.test_moving_cannon.v_y, 0)

    # def test_move(self):
    #     #self.test_moving_cannon = MovingCannon(x = 100, y = 100, v_x = 7, v_y = 7, move_x = 0, move_y = 0)
    #     self.test_moving_cannon = MovingCannon(x = 100, y = 100, v_x = 7, v_y = 7)
    #     self.test_moving_cannon.move()
    #     self.assertEqual(self.test_moving_cannon.move_x, 0)
    # def test_move_right(self):
    #     self.test_moving_cannon.move_right()
    # def test_move_left(self):
    #     self.test_moving_cannon = MovingCannon.move(self, screen_size = [0,1])
    # def test_move_up(self):
    #     self.test_moving_cannon = MovingCannon.move()
    # def test_move_down(self):
    #     self.test_moving_cannon = MovingCannon.move()

# class TestArtificialCannon(unittest.TestCase):
#     def test_init(self):
#         self.test_artificial_cannon = ArtificialCannon(x = 100, y = 100, v_x = 3, v_y = 3)
#         self.assertEqual(self.test_artificial_cannon.v_x, 3)
#         self.assertEqual(self.test_artificial_cannon.v_y, 3)
    
#         self.assertIsNone(self.test_artificial_cannon.strike_thread, None)
    
#     def test_determine_move(self):
#         self.test_artificial_cannon = ArtificialCannon(x = 100, y = 100, v_x = 3, v_y = 3)
#         self.test_artificial_cannon.determine_move()


# class TestTargets(unittest.TestCase):
#     def setUp(self):

#     def test_init(self):

class TestProjectiles(unittest.TestCase):
    def test_init(self):
        self.test_projectile = ProjectileMaster()

   # def test_create_projectile(self):
    #    self.test_projectile = 




    
    

if __name__ == "__main__":
    unittest.main()


    
