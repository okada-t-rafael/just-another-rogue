from __future__ import annotations

import numpy as np
import typing as t
from tcod.console import Console

from just_another_rogue import tile_types

if t.TYPE_CHECKING:
    from just_another_rogue.engine import Engine
    from just_another_rogue.entity import Entity


class GameMap:
    """
    Class GameMap holds information regarding the map size and tiles. Has
        methods to render itself and to evaluate whether a coordinate is within
        its bounds.
    Properties:
        einge (Engine): Engine related to this map.
        width (int): Width of this map.
        height (int): Height of this map.
        entities (Set[Entity]): Is a set, which behaves kind of like a list
            enforces uniqueness. That is, we can't add an Entity to the set
            twice, where as a list would allow that.
        tiles (np.ndarray): 2D array filled with tiles representing the wall.
        visible (np.ndarray): Tiles the player can currently see
        explored (np.ndarray): Tiles the player has seen before
    """
    def __init__(
        self,
        engine: Engine,
        width: int,
        height: int,
        entities: t.Iterable[Entity] = ()
    ) -> None:

        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)

        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full(
            (width, height), fill_value=False, order="F")
        self.explored = np.full(
            (width, height), fill_value=False, order="F")

    def get_blocking_entity_at_location(
        self,
        location_x: int,
        location_y: int
    ) -> t.Optional[Entity]:
        """
        This function iterates through all the entities, and if one is found
            that is found that blocks movement and occupies the given
            location_x and location_y coordinates, it returns that Entity.
        Parameters:
            location_x (int): The x coordiate of the position that the player
                is trying to move.
            location_y (int): The y coordiate of the position that the player
                is trying to move.
        Return:
            Optional[Entity]: Returns the entity that is blocking the position
                that the player is trying to move to.
        """
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Method in_bounds responsibility is to check whether the given coords
            x and y are within the bounds of this map.
        Parameters:
            x (int): The x coordinate of the position to be evaluated.
            y (int): The y coordinate of the position to be evaluated.
        Returns:
            bool: True if the position is within the bonds of this map.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map. If a tile is in the "visible" array, then draw it with
            the "light" colors. If it isn't, but it's in the "explored" array,
            then draw it with the "dark" color. Otherwise, the default is
            "SHROUD".
        Parameters:
            console (Console): A console object containing a grid of characters
                with foreground/background colors.
        Note:
            Using Console class's tiles_rgb method, we can quickly render the
                entire map. This method proves much faster than using the
                console.print method that we use for the individual entitites.
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, entity.color)
