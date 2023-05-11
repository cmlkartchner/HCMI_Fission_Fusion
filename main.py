from math import cos, sin

import pygame
from Model.AgentEngine.AgentEngine import AgentEngine

from Model.World.__init__ import World


def main():
    # variable declarations
    screen_x = 1600
    screen_y = 900

    pygame.init()  # initilizes the pygame module
    screen = pygame.display.set_mode(
        (screen_x, screen_y))  # sets the pixal size
    screen.fill((0, 0, 0))  # sets the background color
    clock = pygame.time.Clock()  # tracks the amount of time passing

    # this is how many hexes we will use with our
    world = World(int(screen_x*.2125), int(screen_y*.183))
    agentEngine = AgentEngine(world, numAgents=37)

    time_delay = 100
    agent_move_event = pygame.USEREVENT+1
    pygame.time.set_timer(agent_move_event, time_delay)

    world_timed_update_event = pygame.USEREVENT+2
    pygame.time.set_timer(world_timed_update_event, time_delay)

    terminated = False
    while not terminated:
        clock.tick(50)
        world.render(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
                break
            elif event.type == agent_move_event:
                agentEngine.update(time_delay, screen)
            elif event.type == world_timed_update_event:
                world.hexGrid.timed_update(time_delay)

    pygame.display.quit()


if __name__ == '__main__':
    main()
