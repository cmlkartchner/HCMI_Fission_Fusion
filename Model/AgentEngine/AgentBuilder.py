import random

from Model.Agent.Agent import Agent
from Model.AgentEngine.Memory import Memory


def build(numAgents,grid):
    agents = []
    location = random.choice(list(grid.hexagons.keys()))
    
    hexes = grid.get_nAdjacent_cells(location,numAgents-1)
    hexes.append(grid.hexagons.get(location))

    for i in range(numAgents):
        memory = Memory(grid.hexagons)
        agent = Agent(i,hexes[i],memory)
        agents.append(agent)

    return agents
