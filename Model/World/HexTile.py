"""
Created on Sun Jan 23 14:07:18 2022

@author: richa
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame


@dataclass
class HexTile:
    """Creates a Hexagon tile"""

    # radius: float
    # position: Tuple[float, float]
    # row: int
    # col: int
    # colour: Tuple[int, ...]
    # highlight_offset: int = 3
    # max_highlight_ticks: int = 15

    def __init__(self, radius, position, row, col, colour):
        self.radius = radius
        self.position = position
        self.row = row
        self.col = col
        self.colour = colour

        #visual attributes
        self.highlight_offset = 3
        self.max_highlight_ticks = 15
        self.highlight_tick = 0

        self.vertices = self.compute_vertices()
        
        # Keeping track of things situated on the tile
        self.site=None
        self.agent=None
        self.trail=0

        #Hex coordinates
        self.q = self.col
        self.r = self.row - (self.col - (self.col & 1)) / 2
        self.s = -(self.q + self.r)

        self.immediateNeighbors = {}

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1
        
        if self.trail > 0:
            self.trail -= 1

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]

    def get_immediate_neighbors(self, hexagons) -> List[HexTile]:
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        if self.immediateNeighbors:
            return self.immediateNeighbors

        for dir in directions:
            if hexagons.get((self.q+dir[0], self.r+dir[1])):
                self.immediateNeighbors[(self.q+dir[0], self.r+dir[1])] = hexagons.get((self.q+dir[0], self.r+dir[1]))

        return self.immediateNeighbors

    def get_random_neighbor(self, hexagons) -> HexTile:
        if not self.immediateNeighbors:
            self.get_immediate_neighbors(hexagons)

        return random.choice(self.immediateNeighbors.values())


    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def render(self, screen, border_colour, render_highlight=False) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)

        if render_highlight:
            pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def computeDistance(self, other):
        return max(abs(self.q - other.q), abs(self.r - other.r), abs(self.s - other.s))

    #Color the hex if it's a site
    def setColour(self, colour):
        self.colour = colour
    
    #Initialize the hex as a site
    def setSite(self, site):
        self.site=site

    #If there's a site agent or trail on the tile
    def isOfInterest(self):
        return (self.site or self.agent or self.trail)!=False

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return x, y + self.radius

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the hexagon tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)


class FlatTopHexagonTile(HexTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return x, y + self.minimal_radius

    
