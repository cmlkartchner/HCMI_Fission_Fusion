from math import cos,sin

import pygame
from Model.AgentEngine.AgentEngine import AgentEngine

from Model.World.__init__ import World

def main():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    world = World(340,170)
    agentEngine = AgentEngine(2, world)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        world.render(screen)
        agentEngine.update(screen)
        clock.tick(50)
    pygame.display.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
