import random

from Model.Agent.Agent import Agent
from Model.AgentEngine.AgentMemory import AgentMemoryTimedDict

def build(numAgents,grid):
    agents = []
    location = random.choice(list(grid.hexagons.keys()))
    
    hexes = grid.get_nAdjacent_cells(location,numAgents-1)
    hexes.append(grid.hexagons.get(location))

    for i in range(numAgents):
        memory = AgentMemoryTimedDict(20)
        agent = Agent(i,hexes[i],memory, 0.1/numAgents)
        agents.append(agent)
    return agents
