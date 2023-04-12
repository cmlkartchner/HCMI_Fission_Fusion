from Model.Agent.State import ExploreState, GroupState, State, YearningState
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

            # Agent should only move if enough time has passed since the last update
            if self.move_timers[agent] >= 1000/agent.getMovementSpeed():

                self.setStateBehavior(agent)

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

    
    def setStateBehavior(self, agent):
        #Identifying agents in comfort radius to determine if state change is possible
        reading = self.grid.get_rDistance_reading(agent.hex, agent.comfort_radius, SensorReading())
        if not reading.agents and isinstance(agent.state, GroupState):
            agent.setState(ExploreState())
        
        elif reading.agents and isinstance(agent.state, ExploreState):
            if agent.state.timer>=20:
                agent.setState(GroupState())
      
        elif not reading.agents and isinstance(agent.state, ExploreState) and agent.state.timer>=40:
            agent.cached_state = agent.state
            agent.setState(YearningState())
            print("Agent ", agent.id, "changed from explore state to yearning state")

            directionGroups = [[(1,-1), (1,0)], [(-1,1), (0,1)], [(0,-1), (1,0)]]

            reading = SensorReading()
            for a in self.agents:
                # sensorReading.agents[hexLocation]=hex.agents
                if (a.hex.q,a.hex.r) in reading.agents:
                    reading.agents[(a.hex.q,a.hex.r)].add(a)
                else:
                    reading.agents[(a.hex.q,a.hex.r)] = set([a])
            
            availableMoves = self.grid.get_immediate_neighbors(agent.hex)
            agent.updateAvailableMoves(availableMoves)
            intentHex = agent.getIntent(reading)

            for group in directionGroups:
                if (intentHex.q - agent.hex.q, intentHex.r - agent.hex.r) in group:
                    agent.state.setDirection(group)
                    break

        elif isinstance(agent.state, YearningState):
            reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
            if reading.agents:
                agent.setState(agent.cached_state)
                print("Agent ", agent.id, "changed back from yearning state to explore state")


