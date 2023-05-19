import math
import random

# NOTES TO SELF: looks like every state has a getSpeedMultiplier
# other methods for each state are at least somewhat unique to that state

class State:
    def __init__(self, color, agent):
        self.color = color # The color that will display on the grid
        self.timer = 0 # The timer that tracks how long an agent has been in a state
        self.agent = agent # The agent the state is attached to; reference to context
    
    """A method to be overridden by children states.
       dt: an int indicating how many milliseconds have passed"""
    def update(self, dt):
        self.timer += dt/1000   # to convert dt to seconds

    """Calculates a decision vector based on pheromone trail finding.
       trails: a vector of HexTiles
       returns a vector of ints (or floats?)"""
    def findTrail(self, trails):
        decisionVectors = []
        if trails:
            for trailHex in trails.values():
                if self.agent.hex.computeDistance(trailHex):
                    q,r = self.agent.get_step_to_target(trailHex)
                    # getting hex's relative position to self.agent.hex
                    q,r = q-self.agent.hex.q, r-self.agent.hex.r

                    total_pheromone_strength=0
                    for item in trailHex.trail:
                        id, pheromone_strength, timer, sacredTimer = item
                        if id!=self.agent.id:
                            total_pheromone_strength += pheromone_strength
                        
                    total_pheromone_strength/=1000
                    intent = total_pheromone_strength/(self.agent.hex.computeDistance(trailHex))**2
                    intent *= self.getIntentToTrailMultiplier()
                        
                    decisionVectors.append((q,r,intent))
        return decisionVectors

    """Calculates a decision vector based on site finding.
        sites: a vector of Sites
        returns a vector of ints"""
    def findSite(self, sites):
        decisionVectors = []
        if sites:
            for loc in sites.keys():
                if not self.agent.memory.contains(loc):
                    site = sites[loc]

                    # NOTE: BEST SITE STUFF IS FOR BEST-OF-N AGENTS
                    if self.agent.memory.best_site == None:
                        self.agent.memory.set_best_site(site)
                    elif site.getQuality() > self.agent.memory.best_site.getQuality():
                        self.agent.memory.set_best_site(site)

                    if self.agent.hex.computeDistance(site.hex):
                        q,r = self.agent.get_step_to_target(site.hex)
                        q,r = q-self.agent.hex.q, r-self.agent.hex.r

                        intent = site.quality/(self.agent.hex.computeDistance(site.hex))**2
                        intent *= self.getIntentToSiteMultiplier()

                        decisionVectors.append((q,r,intent))
        return decisionVectors

    """Calculates a decision vector based on finding neighbor agents.
        agents: a vector of Agents
        returns a vector of ints"""
    def findNeighbors(self, agents):
        decisionVectors = []
        if agents:
            for agents in agents.values():
                for agent in agents:
                    if self.agent.hex.computeDistance(agent.hex):
                        q,r = self.agent.get_step_to_target(agent.hex)
                        q,r = q-self.agent.hex.q, r-self.agent.hex.r

                        intent = self.agent.getAttractionCoefficient(agent)/(self.agent.hex.computeDistance(agent.hex))**2
                        intent *= self.getIntentToAgentMultiplier()

                        decisionVectors.append((q,r,intent))
        return decisionVectors

class GroupState(State):
    def __init__(self, agent):
        super().__init__((30,144,255), agent) # blue
        self.lethargyTimer=10
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToSiteMultiplier(self):
        return 1
    
    def getSpeedMultiplier(self):
        return 1

class ExploreState(State):
    def __init__(self, agent):
        super().__init__((253, 218, 13), agent) # yellow
        self.inflection = 20
        self.exploreTimer = 40

    def update(self, dt, reading):
        super().update(dt)
        decisionVectors = []
        decisionVectors.append(super().findTrail(reading.trails))

        if reading.sites and self.timer > self.agent.state_threshold:
            # TODO: minor thing but fix the assess transition to activate when the agent arrives at a site
            decisionVectors.append(super().findSite(reading.sites))
            self.agent.setState(CanvasState(self.agent))
        
        elif reading.agents:
            decisionVectors.append(super().findNeighbors(reading.agents))
            for agents in reading.agents.values():
                for agent in agents:
                    if isinstance(agent.state, CanvasState) or isinstance(agent.state, LeadingState):
                        siteToConsider = agent.memory.best_site
                        if siteToConsider.quality > self.agent.best_site.quality:
                            self.agent.target_agent = agent
                            self.agent.setState(FollowState(self.agent))

        return decisionVectors
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        if self.timer>self.inflection:
            return -5*((self.inflection-self.timer)/self.timer)
        else:
            return 0

    def getIntentToTrailMultiplier(self):
        if self.timer>self.inflection:
            return -2*((self.inflection-self.timer)/self.timer)
        else:
            return 0

    def getIntentToSiteMultiplier(self):

        # intent to site Multiplier follows exponential decay
        return 0.9 * math.exp(-0.2 * self.timer) + 1.1
    
    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2


class YearningState(State):
    def __init__(self, agent):
        super().__init__((255, 0, 255), agent) # pink

    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2

class RebelState(State):
    def __init__(self, agent):
        super().__init__((112, 41, 99), agent) # red
        self.direction=None

        # Agent will stay in this state for anywhere between 4 to 10s 
        self.tiredTimer = random.randint(4, 10)

    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2

    def setDirection(self,direction):
        self.direction=direction
    

# Not implemented
class PredatorState(State):
    def __init__(self):
        super().__init__((210, 43, 43)) # red
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1

########## BEST-OF-N STATES ##########
# NOTE: we'll use the base ExploreState haha
# TODO: implement Assess and Canvas states first. The transition to the Carry states can be filled with Explore state for now;

class CanvasState(State):
    def __init__(self, agent):
        super().__init__((30, 144, 255), agent) # blue

    def update(self, dt, reading):
        super().update(dt)
        decisionVectors = []
        decisionVectors.append(super().findTrail(reading.trails))
        decisionVectors.append(super().findNeighbors(reading.agents))
        # TODO: implement state behavior, return decisionVector
        if self.timer < self.agent.state_threshold:
            if reading.agents:
                for agents in reading.agents.values():
                    for agent in agents:
                        if isinstance(agent.state, FollowState):
                            self.agent.setState(LeadingState(self.agent))
                            break
        else:
            self.agent.setState(ExploreState(self.agent))
        return decisionVectors

    def getIntentToSiteMultiplier(self):
        return 1
    
    def getIntentToAgentMultiplier(self):
        return 3

    def getIntentToTrailMultiplier(self):
        return 2
    
    def getSpeedMultiplier(self):
        return 2

class LeadingState(State):
    def __init__(self, agent):
        super().__init__((112, 41, 99), agent) # red

    def update(self, dt, reading):
        super().update(dt)
        # TODO: implement state behavior, return decisionVector
        # move toward target neighbor
        # if arrived:
        #   transition to AssessState
        # if getLost:
        #   transition to ExploreState

    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1
    
    def getSpeedMultiplier(self):
        return 2

class FollowState(State):
    def __init__(self, agent):
        super().__init__((255, 0, 255), agent) # green

    def update(self, dt, reading):
        super().update(dt)
        # TODO: implement state behavior, return decisionVector
        # move toward target site
        # if arrived:
        #   transition to ExploreState
        # if lostNeighbor:
        #   transition to CanvasState

    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1
    
    def getSpeedMultiplier(self):
        return 2
    