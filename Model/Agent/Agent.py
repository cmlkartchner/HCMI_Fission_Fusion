from .State import State

class Agent:
    def __init__(self, id, hex, memory, pheromone_strength=5, health=100, movement_speed=1):
        self.id = id
        self.health = health
        self.movement_speed = movement_speed
        self.hex = hex
        self.situate_at_hex(hex)
        
        self.state = State.GROUP
        self.max_movement_speed = self.movement_speed*2
        self.sensing_radius = 20
        self.memory = memory
        self.pheromone_strength = pheromone_strength

    
    #Moves the agent from one cell to a neighbor. 

    def move(self,to):
        self.remove_from_hex(self.hex)
        self.hex.trail += self.pheromone_strength
        
        nextHex = self.possible_moves.get(to)
        self.situate_at_hex(nextHex)        

    def situate_at_hex(self,hex):
        self.inspect()

        self.hexUnadulteredColour = hex.getColour()
        hex.setColour((128, 0, 0))
        hex.addAgent(self)
        self.hex=hex
    
    def remove_from_hex(self,hex):
        hex.setColour(self.hexUnadulteredColour)
        hex.removeAgent(self)


    #Agent's Sensor reading is used to update decision vectors
    def updateReading(self, reading):
        pass

    #Gets neighboring cells the agent can move to
    def updateAvailableMoves(self, availableMoves):
        self.possible_moves = availableMoves


    #Inspects the hex it is currently at and adds its information to memory
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