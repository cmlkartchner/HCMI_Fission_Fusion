def getReading(hexagons, location, radius):
    directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    for r in range(1,radius):
        for d in directions:
            x = location[0] + d[0] * r
            y = location[1] + d[1] * r
            if x >= 0 and x < len(hexagons) and y >= 0 and y < len(hexagons[0]):
                if hexagons[x][y] == 1:
                    return True
    return False
    
