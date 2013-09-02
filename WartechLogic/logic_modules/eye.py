class EyeModule(object):
    def __init__(self, fighter, module):
        self.fighter = fighter
        self.module = module

    def process(self):
        x, y, direction = self.fighter.x, self.fighter.y, self.fighter.direction