import random

from Model.Agent.Agent import Agent

def build(numAgents,grid):
    agents = []
    location = random.choice(list(grid.hexagons.keys()))
    
    hexes = grid.get_nAdjacent_cells(location,numAgents-1)
    hexes.append(grid.hexagons.get(location))

    for i in range(numAgents):
        memory = {key:-1 for key in grid.hexagons.keys()}
        agent = Agent(i,hexes[i],memory)
        agents.append(agent)
    return agents
