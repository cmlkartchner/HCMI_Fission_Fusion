import math


class State:
    def __init__(self, color):
        self.color = color
        self.timer = 0
    
    def update(self, dt):
        self.timer += dt/1000   # to convert dt to seconds

class GroupState(State):
    def __init__(self):
        super().__init__((30,144,255)) # blue
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToSiteMultiplier(self):
        return 1
    
    def getSpeedMultiplier(self):
        return 1

class ExploreState(State):
    def __init__(self):
        super().__init__((253, 218, 13)) # yellow
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        if self.timer>10:
        # Intent to agent Multiplier is a parabolic curve with a minima at timer=10
            return -5*((10-self.timer)/self.timer)

    def getIntentToTrailMultiplier(self):
        if self.timer>10:
            return -2*((10-self.timer)/self.timer)

    def getIntentToSiteMultiplier(self):

        # intent to site Multiplier follows exponential decay
        return 0.9 * math.exp(-0.2 * self.timer) + 1.1
    
    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2


class YearningState(State):
    def __init__(self):
        super().__init__((255, 192, 203)) # pink

    

class PredatorState(State):
    def __init__(self):
        super().__init__((210, 43, 43)) # red
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1
    