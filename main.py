from math import cos, sin

import pygame
from Model.AgentEngine.AgentEngine import AgentEngine

from Model.World.__init__ import World


def main():
    pygame.init()  # initiliaze pygame and all the moduels with it
    screen = pygame.display.set_mode((1000, 900))  # set the screen size
    screen.fill((0, 0, 0))  # fill the screen with black
    clock = pygame.time.Clock()  # create a clock object to track time

    # creates a world object. The variables are the amount of hexagons in the X and Y direction. Starts in the top left corner
    world = World(340, 170)

    # basically this is setting up a list of 37 agents to be placed on a random hex of seven hexagons in the previously made world
    agentEngine = AgentEngine(world, numAgents=37)

    time_delay = 100  # not sure how many seconds or when exactly this comes in, come back to
    agent_move_event = pygame.USEREVENT+1
    pygame.time.set_timer(agent_move_event, time_delay)

    world_timed_update_event = pygame.USEREVENT+2
    pygame.time.set_timer(world_timed_update_event, time_delay)

    terminated = False
    while not terminated:
        clock.tick(50)  # this keeps the speed limited to 50 frames per second
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
