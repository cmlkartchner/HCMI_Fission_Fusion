import AgentBuilder
from SensorReading import SensorReading

class AgentEngine:

    def __init__(self, numAgents, world):
        self.grid = world.hexGrid
        self.agents = AgentBuilder.build(numAgents, world.hexGrid)

    def update(self):
        for agent in self.agents:
            reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
            agent.updateReading(reading)