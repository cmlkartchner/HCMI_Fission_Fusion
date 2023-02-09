class Sensor:

    def __init__(self, hexagons):
        self.hexagons = hexagons


    def getReading(self, hexagons, location, radius):
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        locations_of_interest = {}

        #get the neighbors of hex starting from the one in the immediate right and going clockwise
        for r in range(1,radius):
            
            #this loop gets the neighbours that lie exactly in the six directions
            for i in range(len(directions)):
                x = location[0] + directions[i][0] * r
                y = location[1] + directions[i][1] * r
                
                if self.hexagons.get((x,y)):
                    hex = self.hexagons.get((x,y))
                    items_of_interest=[]
                    if hex.agent:
                        items_of_interest.append(hex.agent)
                    if hex.site:
                        items_of_interest.append(hex.site)
                    if hex.trail:
                        items_of_interest.append(hex.trail)
                    if items_of_interest:
                        locations_of_interest[(x,y)] = items_of_interest

                #this one takes care of in-betweener hexes for radius>=2
                for j in range(1,r):
                    
                    #The directions for in-betweener hexes can be obtained by offsetting the 6-directional array by 2 indices
                    offsetIndex = (i+2)%6
                    nx = x + directions[offsetIndex]*j
                    ny = y + directions[offsetIndex]*j

                    neighbors.append((nx,ny))

        return False
    
