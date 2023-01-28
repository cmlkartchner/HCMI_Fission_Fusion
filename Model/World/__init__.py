from .HexGrid import HexGrid

class World:

    def __init__(self, num_x, num_y):
        self.hexGrid = HexGrid(num_x, num_y)

    def render(self,screen):
        self.hexGrid.render(screen)