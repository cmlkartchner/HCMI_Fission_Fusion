from . import AgentBuilder
from Model.AgentEngine.SensorReading import SensorReading

class AgentEngine:

    def __init__(self, world, numAgents):
        self.grid = world.hexGrid
        self.agents = AgentBuilder.build(numAgents, world.hexGrid)

        for agent in self.agents:
            agent.attach_observer(self)

    def update(self,screen):
        for agent in self.agents:
            reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
            availableMoves = self.grid.get_immediate_neighbors(agent.hex)
            agent.updateAvailableMoves(availableMoves)
            agent.move(agent.getIntent(reading))
    
    def notify(self, agent):
        reading = self.grid.get_rDistance_reading(agent.hex, agent.communication_radius, SensorReading())
        agent.set_nearby_agents(reading.agents)
