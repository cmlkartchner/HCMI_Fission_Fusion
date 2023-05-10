import random
from Model.Agent.State import ExploreState, GroupState, RebelState, State, YearningState
from . import AgentBuilder
from Model.AgentEngine.SensorReading import SensorReading

# NOTE TO SELF: The AgentEngine class is what does decision-making n tandem with
# Agent. AgentEngine seems like a blackboard (possible tie-in to BTs?).
# Do we want to make the states follow the state pattern?
# Would have to rewrite AgentEngine... aka have the decision-making within the State classes themselves

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

                # self.setStateBehavior(agent)

                # Identifying objects in sensing radius to determine intent;
                # dependent on state
                # NOTE: YearningState would call self.getAllAgentsInReading()
                reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())

                # Calculate possible movements and move agent
                availableMoves = self.grid.get_immediate_neighbors(agent.hex)
                agent.updateAvailableMoves(availableMoves)
                agent.move(agent.getIntent(self.move_timers[agent], reading)) # NOTE: This is where Agent.getIntent is called

                # For the agent to keep track of time spent in state
                # agent.state.update(self.move_timers[agent]) # NOTE: This is where State.update() is called, dt passed in is self.move_timers[agent]
                self.move_timers[agent] = 0
    
    def notify(self, agent):

        #Identifying agents in communication radius
        reading = self.grid.get_rDistance_reading(agent.hex, agent.communication_radius, SensorReading())
        agent.set_nearby_agents(reading.agents)

    """Changes the state of an agent. Includes transition logic for the states."""
    # TODO: put transition logic in the states themselves
    def setStateBehavior(self, agent):

        directions = [(1,-1), (1,0), (-1,1), (0,1), (0,-1), (1,0)]
        #Identifying agents in comfort radius to determine if state change is possible
        reading = self.grid.get_rDistance_reading(agent.hex, agent.comfort_radius, SensorReading())

        # STATE TRANSITIONS
        if not reading.agents and isinstance(agent.state, GroupState):
            agent.setState(ExploreState(agent))

        elif isinstance(agent.state, GroupState) and reading.agents and agent.state.timer>agent.state.lethargyTimer:
            rebelFlag = True
            for otherAgent in self.agents:
                if not otherAgent==agent and isinstance(otherAgent.state, RebelState):
                    rebelFlag = False
                    break
            
            # introducing some randomness to the rebelState
            if rebelFlag and random.random() < 0.01:
                agent.setState(RebelState())
                agent.state.setDirection(random.choice(directions))

        elif isinstance(agent.state, RebelState) and agent.state.timer>=agent.state.tiredTimer:
            agent.setState(ExploreState(agent))

        
        elif reading.agents and isinstance(agent.state, ExploreState):
            if agent.state.timer>=20:
                agent.setState(GroupState())

                # communicating the three most recent sites the agent has visited to other agents
                comms = agent.memory.get_n_most_recent(3)
                for otherAgents in reading.agents.values():
                    for otherAgent in otherAgents:
                        for location, value, timestamp in comms:
                            otherAgent.add_to_memory(value, location, timestamp)
      
        elif not reading.agents and isinstance(agent.state, ExploreState) and agent.state.timer>=agent.state.exploreTimer:
            agent.cached_state = agent.state
            agent.setState(YearningState())

        elif isinstance(agent.state, YearningState):
            reading = self.grid.get_rDistance_reading(agent.hex, agent.sensing_radius, SensorReading())
            if reading.agents:
                agent.cached_state.exploreTimer+=agent.cached_state.exploreTimer
                agent.setState(agent.cached_state)
    

    def getAllAgentsInReading(self):
        reading = SensorReading()
        
        for a in self.agents:
            # sensorReading.agents[hexLocation]=hex.agents
            if (a.hex.q,a.hex.r) in reading.agents:
                reading.agents[(a.hex.q,a.hex.r)].add(a)
            else:
                reading.agents[(a.hex.q,a.hex.r)] = set([a])

        return reading


