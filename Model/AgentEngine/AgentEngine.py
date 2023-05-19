import random
from Model.Agent.State import ExploreState, GroupState, RebelState, State, YearningState
from . import AgentBuilder
from Model.AgentEngine.SensorReading import SensorReading

# NOTE TO SELF: The AgentEngine class is what does decision-making n tandem with
# Agent. AgentEngine seems like a blackboard (possible tie-in to BTs?).

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

            # Agent should only move if enough time has passed since the last update
            if self.move_timers[agent] >= 1000/agent.getMovementSpeed():

                # Identifying objects in sensing radius to determine intent;
                # dependent on state
                # NOTE: YearningState would call self.getAllAgentsInReading()
                reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())

                # Calculate possible movements and move agent
                availableMoves = self.grid.get_immediate_neighbors(agent.hex)
                agent.updateAvailableMoves(availableMoves)
                agent.move(agent.getIntent(self.move_timers[agent], reading))

                # For the agent to keep track of time spent in state
                self.move_timers[agent] = 0
    
    def notify(self, agent):

        #Identifying agents in communication radius
        reading = self.grid.get_rDistance_reading(agent.hex, agent.communication_radius, SensorReading())
        agent.set_nearby_agents(reading.agents)
    

    def getAllAgentsInReading(self):
        reading = SensorReading()
        
        for a in self.agents:
            # sensorReading.agents[hexLocation]=hex.agents
            if (a.hex.q,a.hex.r) in reading.agents:
                reading.agents[(a.hex.q,a.hex.r)].add(a)
            else:
                reading.agents[(a.hex.q,a.hex.r)] = set([a])

        return reading


