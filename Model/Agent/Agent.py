from .State import State

class Agent:
    def __init__(self, id, hex, memory, pheromone_strength=5, health=100, movement_speed=1):
        self.id = id
        self.health = health
        self.movement_speed = movement_speed
        self.hex = hex
        
        self.state = State.GROUP
        self.max_movement_speed = self.movement_speed*2
        self.sensing_radius = 20
        self.memory = memory
        self.pheromone_strength = pheromone_strength

        self.situate_at_hex(hex)

    
    #Moves the agent from one cell to a neighbor. 

    def move(self,to):
        self.remove_from_hex(self.hex)
        
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
        self.hex.trail += self.pheromone_strength
        hex.removeAgent(self)


    #Agent's Sensor reading is used to update decision vectors
    def updateReading(self, reading):
        self.decisionVectors = []
        if self.state == State.EXPLORE:
            if reading.trails:
                for trailHex in reading.trails.Values():
                    q,r = self.get_step_to_target(trailHex)

                    intent = trailHex.trail/(self.hex.computeDistance(trailHex))**2
                    hex = self.possible_moves.get((q,r))
                    self.decisionVectors.append((hex,intent))

        if reading.sites:
            for site in reading.sites.values():
                q,r = self.get_step_to_target(site.hex)
                
                intent = site.quality/(self.hex.computeDistance(site.hex))**2
                hex = self.possible_moves.get((q,r))
                self.decisionVectors.append((hex,intent))
        
        if reading.agents:
            for agents in reading.agents.values():
                for agent in agents:
                    q,r = self.get_step_to_target(agent.hex)

                    intent = self.getAttractionCoefficient(agent)/(self.hex.computeDistance(agent.hex))**2
                    hex = self.possible_moves.get((q,r))
                    self.decisionVectors.append((hex,intent))



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
    

    #Gets next hex to move to in order to reach target
    def get_step_to_target(self, target):
        distance_to_target = self.hex.computeDistance(target)

        q = self.linearInterpolate(self.hex.q, target.q, 1/distance_to_target)
        r = self.linearInterpolate(self.hex.r, target.r, 1/distance_to_target)
        s = self.linearInterpolate(self.hex.s, target.s, 1/distance_to_target)

        q,r,s = self.round_to_hexCoordinates(q, r, s)

        return q,r


    def linearInterpolate(self, a, b, multiplier):
        return a + (b-a) * multiplier

    def round_to_hexCoordinates(self,q,r,s):
        round_q = round(q)
        round_r = round(r)
        round_s = round(s)

        q_diff = abs(round_q - q)
        r_diff = abs(round_r - r)
        s_diff = abs(round_s - s)

        if q_diff > r_diff and q_diff > s_diff:
            round_q = -round_r-round_s
        elif r_diff > s_diff:
            round_r = -round_q-round_s
        else:
            round_s = -round_q-round_r

        return round_q, round_r, round_s
    
    #Calculates the attraction between agents
    def getAttractionCoefficient(self,other):
        return 0.01
