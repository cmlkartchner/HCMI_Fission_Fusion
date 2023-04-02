import math


class State:
    def __init__(self, color):
        self.color = color
        self.timer = 0
    
    def update(self):
        self.timer += 1

class GroupState(State):
    def __init__(self):
        super().__init__((30,144,255)) # blue

    """The direction multiplier can be +1 or -1 and is just used to ascertain direction
    Intent multiplier gives the magnitude of intent 
    Together the two multipliers determine how much the agent wants to move in a particular direction"""

    # Direction Multiplier
    def getAgentDirectionMultiplier(self):
        return 1
    
    def getSiteDirectionMultiplier(self):
        return 1
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToSiteMultiplier(self):
        return 1
    
class ExploreState(State):
    def __init__(self):
        super().__init__((253, 218, 13)) # yellow

    # Direction Multiplier 
    def getTrailDirectionMultiplier(self):
        if self.timer <= 20:
            return -1
        else:
            return 1

    def getAgentDirectionMultiplier(self):
        if self.timer <= 20:
            return -1
        else:
            return 1
    
    def getSiteDirectionMultiplier(self):
        return 1
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):

        # Intent to agent Multiplier is a parabolic curve with a minima at timer=20
        if self.timer<=40:
            return 0.01225*(self.timer**2)-0.49*(self.timer)+5
        else:
            return 5 

    def getIntentToTrailMultiplier(self):
        if self.timer<=40:
            return 0.00475*(self.timer**2)-0.19*(self.timer)+2
        else:
            return 5 

    def getIntentToSiteMultiplier(self):

        # intent to site Multiplier follows exponential decay
        return 0.9 * math.exp(-0.1 * self.timer) + 1.1

class PredatorState(State):
    def __init__(self):
        super().__init__((210, 43, 43)) # red

    # Direction Multiplier
    def getTrailDirectionMultiplier(self):
        return 1

    def getAgentDirectionMultiplier(self):
        return 1
    
    # Intent Multiplier 
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1
    