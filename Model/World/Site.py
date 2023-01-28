
class Site:
    """ Represents areas the agents would want to explore """
    def __init__(self, hexagon, quality=5):
        self.hex = hexagon
        self.hex.setColour((0,128,0))
        self.hex.setSite(self)

        self.quality = quality
        self.visitors = set()

    def getQuality(self):
        return self.quality
    
    def setQuality(self, quality):
        self.quality = quality

    def getHex(self):
        return self.hex

    def setHex(self, hex):
        self.hex = hex
        self.hex.setColour((0,128,0))
        self.hex.setSite(self)
    
    def getVisitors(self):
        return self.visitors

    def addVisitor(self, visitor):
        self.visitors.add(visitor)



