from .State import State
from .Memory import Memory

class Agent:
    def __init__(self, id, initial_location, hexagons, pheromone_strength=5, health=100, movement_speed=1):
        self.id = id
        self.health = health
        self.movement_speed = movement_speed
        self.hex = initial_location
        
        self.state = State.GROUP
        self.max_movement_speed = self.movement_speed*2
        self.sensing_radius = 5
        self.memory = Memory(hexagons)
        self.pheromone_strength = pheromone_strength

    #Moves the agent from one cell to a neighbor. 
    #Could have the agent keep a copy of the hexgrid to get the hex associated with the position.
    #But agent cannot know about the entire grid without exploring
    #Therefore we need a method on an individual Hextile to find neighbors of that hex

    def initiate_move(self,to):
        self.inspect()

        possible_moves = self.hex.get_immediate_neighbors()
        self.hex.agent = None
        self.hex.trail += self.pheromone_strength
        
        nextHex = possible_moves.get(to)
        self.complete_move(nextHex)
    

    def complete_move(self, nextHex):
        nextHex.agent=self
        self.hex=nextHex


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