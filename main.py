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
    agentEngine = AgentEngine(world, numAgents=4)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        world.render(screen)
        agentEngine.update(screen)
        clock.tick(50)
    pygame.display.quit()


if __name__ == '__main__':
    main()
