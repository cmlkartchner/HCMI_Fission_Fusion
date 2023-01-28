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

    def create_hexagon(self, position, row, col, radius=5, flat_top=False) -> HexTile:
        """Creates a hexagon tile at the specified position"""
        class_ = FlatTopHexagonTile if flat_top else HexTile
        return class_(radius, position, row, col, colour=(5,5,5))


    def init_hexagons(self, flat_top=False) -> List[HexTile]:
        # pylint: disable=invalid-name

        leftRowCoord, leftColCoord = int(-self.num_y / 2), int(-self.num_x / 2)

        leftmost_hexagon = self.create_hexagon((0, 0), leftRowCoord, leftColCoord, flat_top=flat_top)
        hexagons = {(leftmost_hexagon.q, leftmost_hexagon.r) : leftmost_hexagon}
        for x in range(self.num_y):
            if x:
                # alternate between bottom left and bottom right vertices of hexagon above
                index = 2 if x % 2 == 1 or flat_top else 4
                position = leftmost_hexagon.vertices[index]
                leftRowCoord += 1

                leftmost_hexagon = self.create_hexagon(position, leftRowCoord, leftColCoord, flat_top=flat_top)
                hexagons[(leftmost_hexagon.q, leftmost_hexagon.r)] = leftmost_hexagon

            # place hexagons to the left of leftmost hexagon, with equal y-values.
            hexagon = leftmost_hexagon
            colCoord = leftColCoord + 1

            for i in range(self.num_x):
                x, y = hexagon.position  # type: ignore
                if flat_top:
                    if i % 2 == 1:
                        position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                    else:
                        position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
                else:
                    position = (x + hexagon.minimal_radius * 2, y)
                hexagon = self.create_hexagon(position, leftRowCoord, colCoord, flat_top=flat_top)
                hexagons[(hexagon.q, hexagon.r)] = hexagon
                colCoord += 1

        SiteBuilder.build_sites(hexagons, num_sites=40)

        return hexagons

    def getGrid(self):
        return self.hexagons

    def getCell(self,q,r):
        return self.hexagons.get((q,r))

    def render(self,screen):
        """Renders hexagons on the screen"""

        for hexagon in self.hexagons.values():
            hexagon.render(screen, border_colour=(255, 255, 255),render_highlight=False)

        # draw borders around colliding hexagons and neighbours
        mouse_pos = pygame.mouse.get_pos()
        colliding_hexagons = [
            hexagon for hexagon in self.hexagons.values() if hexagon.collide_with_point(mouse_pos)
        ]

        for hexagon in self.hexagons.values():
            hexagon.update()

            # for neighbour in hexagon.compute_neighbours(hexagons):
            #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
            # hexagon.render_highlight(screen, border_colour=(0, 0, 0))
        pygame.display.flip()