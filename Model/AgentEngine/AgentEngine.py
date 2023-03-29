from Model.Agent.State import State
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
            
            #Identifying agents in comfort radius to determine if state change is possible
            reading = self.grid.get_rDistance_reading(agent.hex, agent.comfort_radius, SensorReading())
            if not reading.agents:
                agent.setState(State.EXPLORE)
            
            elif agent.state == State.EXPLORE:
                agent.setState(State.GROUP)
            
            #Identifying objects in sensing radius to determine intent
            reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
            availableMoves = self.grid.get_immediate_neighbors(agent.hex)
            agent.updateAvailableMoves(availableMoves)
            agent.move(agent.getIntent(reading))
    
    def notify(self, agent):

        #Identifying agents in communication radius
        reading = self.grid.get_rDistance_reading(agent.hex, agent.communication_radius, SensorReading())
        agent.set_nearby_agents(reading.agents)

        
