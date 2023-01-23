import HexGrid

class Site:
    """ Represents areas the agents would want to explore """
    def __init__(self, pos, quality, grid):
        self.q = pos[0]
        self.r = pos[1]
        self.quality = quality
        self.visitedBy = set()
        self.grid = grid


    def setSite(self):
        hexagon = self.grid.getCell(self.q, self.r)
