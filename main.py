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
