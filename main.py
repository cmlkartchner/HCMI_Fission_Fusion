import math
from math import cos,sin

import pygame

from Model.World.HexGrid import HexGrid

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    hexGrid = HexGrid(150,100)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        hexGrid.render(screen)
        clock.tick(50)
    pygame.display.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
