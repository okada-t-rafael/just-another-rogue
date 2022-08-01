from __future__ import annotations

import copy
import typing as t


if t.TYPE_CHECKING:
    from just_another_rogue.game_map import GameMap

T = t.TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    Properties:
        x (int): The Entitiy's "x" coordinate on the map.
        y (int): The Entitiy's "y" coordinate on the map.
        char (str):  Is the character we'll use to represent the entity. (Our
            player will be an "@" symbol, whereas something like a Troll can be
            the letter "T").
        color (Tuple[int, int, int]): Is the color we'll use when drawing the
            Entity. We define color as a Tuple of three integers, representing
            the entity's RGB values.
        name (str): It's what the Entity is called.
        blocks_movement (bool): Describes whether or not his Entity can be
            moved over or not. Enemies will have blocks_movement set to True,
            things like consumable items and equipment will be set to False.
    """
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: t.Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        game_map: t.Optional[GameMap] = None
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

        if game_map:
            self.game_map = game_map
            self.game_map.entities.add(self)

    def spaws(self: T, game_map: GameMap, x: int, y: int) -> T:
        """
        Spawn a copy of this instance at the given location.
        Parameters:
            gamemap (GameMap): Instance of GameMap that will hold this entity.
            x (int): The x coordinate of the new instance location.
            y (int): The y coordinate of the new instance location.
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        clone.game_map.entities.add(clone)
        return clone

    def place(
        self,
        x: int,
        y: int,
        game_map: t.Optional[GameMap] = None
    ) -> None:
        """
        Place this entity at a new location. Handles moving across GameMaps.
        Parameters:
            x (int): The x coordinate of the new location.
            y (int): The y coordinate of the new locaiton.
            game_map (Optional[GameMap]): The new map of the new location.
        """
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            self.game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        """
        Method move. Move the entity by a given amount.
        Params:
            dx (int): Amount of units to move in the x direciton.
            dy (int): Amount of units to move in the y direciton.
        """
        self.x += dx
        self.y += dy
