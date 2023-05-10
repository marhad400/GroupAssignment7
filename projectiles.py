from inherited import Projectile

class CircleProjectile(Projectile):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''
    def __init__(self, x, y, v_x, v_y, color, size, health):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            x = x, y = y,
            v_x = v_x, v_y = v_y,
            color = color, size = size, health = health,
            shape = 'c')

class SquareProjectile(Projectile):
    def __init__(self, x, y, v_x, v_y, color, size, health):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            x = x, y = y,
            v_x = v_x, v_y = v_y,
            color = color, size = size, health = health,
            shape = 's')
        
class TriangleProjectile(Projectile):
    def __init__(self, x, y, v_x, v_y, color, size, health):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            x = x, y = y,
            v_x = v_x, v_y = v_y,
            color = color, size = size, health = health,
            shape = 't')