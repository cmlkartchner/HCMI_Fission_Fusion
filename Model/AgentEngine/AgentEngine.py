from Model.Agent.State import ExploreState, GroupState, State
from . import AgentBuilder
from Model.AgentEngine.SensorReading import SensorReading

class AgentEngine:

    def __init__(self, world, numAgents):
        self.grid = world.hexGrid
        self.agents = AgentBuilder.build(numAgents, world.hexGrid)

        for agent in self.agents:
            agent.attach_observer(self)

        self.move_timers = {agent: 0 for agent in self.agents}

    def update(self,dt,screen):
        for agent in self.agents:
            self.move_timers[agent] += dt

            if self.move_timers[agent] >= 1000/agent.getMovementSpeed():

                #Identifying agents in comfort radius to determine if state change is possible
                reading = self.grid.get_rDistance_reading(agent.hex, agent.comfort_radius, SensorReading())
                if not reading.agents:
                    agent.setState(ExploreState())
                
                elif isinstance(agent.state, ExploreState):
                    if agent.state.timer>=40:
                        agent.setState(GroupState())
                
                #Identifying objects in sensing radius to determine intent
                reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
                availableMoves = self.grid.get_immediate_neighbors(agent.hex)
                agent.updateAvailableMoves(availableMoves)
                agent.move(agent.getIntent(reading))

                # For the agent to keep track of time spent in state
                agent.state.update(self.move_timers[agent])
                self.move_timers[agent] = 0
    
    def notify(self, agent):

        #Identifying agents in communication radius
        reading = self.grid.get_rDistance_reading(agent.hex, agent.communication_radius, SensorReading())
        agent.set_nearby_agents(reading.agents)

        
