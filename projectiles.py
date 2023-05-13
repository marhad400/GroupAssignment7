from inherited import Projectile

class CircleProjectile(Projectile):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 'c')

class SquareProjectile(Projectile):
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 's')
        
class TriangleProjectile(Projectile):
    def __init__(self, *args, **kwargs):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        super().__init__(
            *args,
            **kwargs,
            shape = 't')