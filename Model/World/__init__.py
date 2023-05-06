from .HexGrid import HexGrid


class World:

    # num_x and num_y are the number of hexagons in the x and y directions
    def __init__(self, num_x, num_y):
        self.hexGrid = HexGrid(num_x, num_y)

    def render(self, screen):
        self.hexGrid.render(screen)
