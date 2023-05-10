import math
import random

# NOTES TO SELF: looks like every state has a getSpeedMultiplier
# other methods for each state are at least somewhat unique to that state


class State:
    def __init__(self, color):
        self.color = color
        self.timer = 0

    def update(self, dt):
        self.timer += dt/1000   # to convert dt to seconds


class GroupState(State):  # gonna be resting instead
    def __init__(self):
        super().__init__((85, 52, 235))  # purple/blue
        self.lethargyTimer = 10

    # Intent Multiplier
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToSiteMultiplier(self):
        return 1

    def getSpeedMultiplier(self):
        return 1


class ExploreState(State):  # will stay explore state
    def __init__(self):
        super().__init__((140, 235, 52))  # green
        self.inflection = 20
        self.exploreTimer = 40

    # Intent Multiplier
    def getIntentToAgentMultiplier(self):
        if self.timer > self.inflection:
            return -5*((self.inflection-self.timer)/self.timer)
        else:
            return 0

    def getIntentToTrailMultiplier(self):
        if self.timer > self.inflection:
            return -2*((self.inflection-self.timer)/self.timer)
        else:
            return 0

    def getIntentToSiteMultiplier(self):

        # intent to site Multiplier follows exponential decay
        return 0.9 * math.exp(-0.2 * self.timer) + 1.1

    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2


class YearningState(State):  # gonna be dancing instead
    def __init__(self):
        super().__init__((235, 52, 128))  # pink

    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2


class RebelState(State):  # gonna be verifying instead
    def __init__(self):
        super().__init__((235, 229, 52))  # yellow
        self.direction = None

        # Agent will stay in this state for anywhere between 4 to 10s
        self.tiredTimer = random.randint(4, 10)

    # Speed multiplier
    def getSpeedMultiplier(self):
        return 2

    def setDirection(self, direction):
        self.direction = direction


# Not implemented
class PredatorState(State):
    def __init__(self):
        super().__init__((210, 43, 43))  # red

    # Intent Multiplier
    def getIntentToAgentMultiplier(self):
        return 1

    def getIntentToTrailMultiplier(self):
        return 1
