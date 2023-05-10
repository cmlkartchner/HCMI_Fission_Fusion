"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple

import pygame
from .HexTile import HexTile
from .HexTile import FlatTopHexagonTile
from .SiteBuilder import SiteBuilder


# pylint: disable=no-member
class HexGrid:
    """Creates a hexGrid of with num_x columns and num_y rows"""

    def __init__(self, num_x, num_y):
        self.num_x = num_x
        self.num_y = num_y
        self.hexagons = self.init_hexagons(flat_top=True)

    def create_hexagon(self, position, row, col, radius=3, flat_top=False) -> HexTile:
        """Creates a hexagon tile at the specified position"""
        #if you change the radius=3 to be a different number then the hexes 
        # will grow and shrink (you don't have to change anything else)
        class_ = FlatTopHexagonTile if flat_top else HexTile
        return class_(radius, position, row, col, colour=(0, 0, 0))

    def init_hexagons(self, flat_top=False) -> List[HexTile]:
        # pylint: disable=invalid-name

        leftRowCoord, leftColCoord = int(-self.num_y / 2), int(-self.num_x / 2)

        leftmost_hexagon = self.create_hexagon(
            (0, 0), leftRowCoord, leftColCoord, flat_top=flat_top)
        hexagons = {(leftmost_hexagon.q, leftmost_hexagon.r): leftmost_hexagon}
        for x in range(self.num_y):
            if x:
                # alternate between bottom left and bottom right vertices of hexagon above
                index = 2 if x % 2 == 1 or flat_top else 4
                position = leftmost_hexagon.vertices[index]
                leftRowCoord += 1

                leftmost_hexagon = self.create_hexagon(
                    position, leftRowCoord, leftColCoord, flat_top=flat_top)
                hexagons[(leftmost_hexagon.q, leftmost_hexagon.r)
                         ] = leftmost_hexagon

            # place hexagons to the left of leftmost hexagon, with equal y-values.
            hexagon = leftmost_hexagon
            colCoord = leftColCoord + 1

            for i in range(self.num_x):
                x, y = hexagon.position  # type: ignore
                if flat_top:
                    if i % 2 == 1:
                        position = (x + hexagon.radius * 3 / 2,
                                    y - hexagon.minimal_radius)
                    else:
                        position = (x + hexagon.radius * 3 / 2,
                                    y + hexagon.minimal_radius)
                else:
                    position = (x + hexagon.minimal_radius * 2, y)
                hexagon = self.create_hexagon(
                    position, leftRowCoord, colCoord, flat_top=flat_top)
                hexagons[(hexagon.q, hexagon.r)] = hexagon
                colCoord += 1

        SiteBuilder.build_sites(hexagons, num_sites=200)

        return hexagons

    def getGrid(self):
        return self.hexagons

    def getCell(self, q, r):
        return self.hexagons.get((q, r))

    def render(self, screen):
        """Renders hexagons on the screen"""

        for hexagon in self.hexagons.values():
            hexagon.render(screen, border_colour=(
                5, 5, 5), render_highlight=True)

        # draw borders around colliding hexagons and neighbours
        # mouse_pos = pygame.mouse.get_pos()
        # colliding_hexagons = [
        #     hexagon for hexagon in self.hexagons.values() if hexagon.collide_with_point(mouse_pos)
        # ]

        for hexagon in self.hexagons.values():
            hexagon.update()

            # for neighbour in hexagon.compute_neighbours(hexagons):
            #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
            # hexagon.render_highlight(screen, border_colour=(0, 0, 0))
        pygame.display.flip()

    # Updates linked to agent actions
    def timed_update(self, dt):

        for hexagon in self.hexagons.values():
            hexagon.timed_update(dt)

    def get_immediate_neighbors(self, hex) -> List[HexTile]:
        """Returns a list of all the immediate neighbors of the hexagon"""
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]

        immediateNeighbors = {}
        q, r = hex.q, hex.r

        for dir in directions:
            if self.hexagons.get((q+dir[0], r+dir[1])):
                immediateNeighbors[(q+dir[0], r+dir[1])
                                   ] = self.hexagons.get((q+dir[0], r+dir[1]))

        return immediateNeighbors

    def get_random_neighbor(self, hex) -> HexTile:
        """Returns a random neighbor of the hexagon"""
        immediateNeighbors = self.get_immediate_neighbors(hex)

        return random.choice(immediateNeighbors.values())

    def get_rDistance_neighbors(self, location, radius):
        """Returns all the hexes that are at a distance r from the given hex"""
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        rDistance_neighbors = []

        # get the neighbors of hex starting from the one in the immediate right and going clockwise
        for r in range(1, radius):

            # this loop gets the neighbours that lie exactly in the six directions
            for i in range(len(directions)):
                x = location[0] + directions[i][0] * r
                y = location[1] + directions[i][1] * r

                if self.hexagons.get((x, y)):
                    rDistance_neighbors.append(self.hexagons.get((x, y)))

                    # this one takes care of in-betweener hexes for radius>=2
                    for j in range(1, r):

                        # The directions for in-betweener hexes can be obtained by offsetting the 
                        # 6-directional array by 2 indices
                        offsetIndex = (i+2) % 6
                        nx = x + directions[offsetIndex][0]*j
                        ny = y + directions[offsetIndex][1]*j

                        if self.hexagons.get((nx, ny)):
                            rDistance_neighbors.append(
                                self.hexagons.get((nx, ny)))

        return rDistance_neighbors

    def get_nAdjacent_cells(self, location, n):
        """this function takes in a location and an integer value n, and returns a list of the n 
        neighboring hexes around the given location."""
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        cells = []

        # get the neighbors of hex starting from the one in the immediate right and going clockwise
        num, r = 0, 1
        while num < n:

            # this loop gets the neighbors that lie exactly in the six directions
            for i in range(len(directions)):
                x = location[0] + directions[i][0] * r
                y = location[1] + directions[i][1] * r

                if self.hexagons.get((x, y)):
                    cells.append(self.hexagons.get((x, y)))
                    num += 1
                    if num == n:
                        return cells

                    # this one takes care of in-betweener hexes for radius>=2
                    for j in range(1, r):

                        # The directions for in-betweener hexes can be obtained by offsetting the 6-directional array by 2 indices
                        offsetIndex = (i+2) % 6
                        nx = x + directions[offsetIndex][0]*j
                        ny = y + directions[offsetIndex][1]*j

                        if self.hexagons.get((nx, ny)):
                            cells.append(self.hexagons.get((nx, ny)))
                            num += 1
                            if num == n:
                                return cells
            r += 1

        return cells

    # passing in a hex value that has a q and r subclass value
    def get_rDistance_reading(self, hex, radius, sensorReading):
        """This function takes in a hex, a radius, and a sensor reading, and then returns an 
        updated sensor reading based on the neighboring hexes within the specified radius."""
        rDistance_neighbors = self.get_rDistance_neighbors(
            (hex.q, hex.r), radius)
        for hex in rDistance_neighbors:  # for each neighboring hex
            hexLocation = (hex.q, hex.r)
            if hex.agents:
                # we change the paramter we're passing in to h
                sensorReading.agents[hexLocation] = hex.agents
            if hex.site:
                sensorReading.sites[hexLocation] = hex.site
            if hex.trail:
                sensorReading.trails[hexLocation] = hex
        return sensorReading
