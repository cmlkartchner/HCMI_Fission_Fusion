from .State import State
from .Memory import Memory

class Agent:
    def __init__(self, id, health, movement_speed, initial_location, hexagons):
        self.id = id
        self.health = health
        self.movement_speed = movement_speed
        self.hex = initial_location
        
        self.state = State.GROUP
        self.max_movement_speed = self.movement_speed*2
        self.sensing_radius = 5
        self.memory = Memory(hexagons)

    def move(self):
        pass

    def inspect(self):
        if self.hex.site:
            self.add_to_memory(self.hex.site.quality)
        else:
            self.add_to_memory(0)

    def add_to_memory(self, value, location=None):
        if location is None:
            location = (self.hex.q,self.hex.r)
        self.memory[location] = value

    def get_from_memory(self, location):
        return self.memory[location]