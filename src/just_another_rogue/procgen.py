from __future__ import annotations

import random
import tcod
import typing as t

from just_another_rogue import entity_factories
from just_another_rogue import tile_types
from just_another_rogue.game_map import GameMap

if t.TYPE_CHECKING:
    from just_another_rogue.engine import Engine


class RectangularRoom:
    """
    ReactanguarRoom is used to create our rooms. It takes the x and y
        coordinates of the top left corner, and computes the bottom right
        corner based on the width and height.
    Properties:
        x1 (int): The x coordinate of the top left corner
        y1 (int): The y coordinate of the top left corner
        x2 (int): The x coordinate of the bottom right corner
        y2 (int): The x coordinate of the bottom right corner
    """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> t.Tuple[int, int]:
        """
        Center is a "property, which essentially acts like a read-only variable
            for our ReactangularRoom class. It describes the "x" and "y"
            coordinates of the center of a room.
        Returns:
            Tuple[int, int]: Returns the coordinates of the center of the room.
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @ property
    def inner(self) -> t.Tuple[slice, slice]:
        """
        The inner property returns two "slices", which represent the inner
            portion of our room. This is the part we'll be "digging out" for
            our room in our dungeon generator. It give us an easy way to get
            the area to carve out.
        Returns:
            Tuple[slice, slice]: Returns the inner area of this room as 2D
                array index.
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """
        Checks if the room and another room intersect or not. It returns True
            if they do, False if they don't. We'll use this to determine if two
            room are overlapping or not.
        Parameters:
            other (RectangularRoom): An instance of RectangularRoom to be
                compared to.
        Returns:
            bool: True if this room overlaps with anorther RectangularRoom.
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(
    room: RectangularRoom,
    dungeon: GameMap,
    maximum_monsters: int
) -> None:
    """
    Function to pu the entities in their place.
    Parameters:
        room (RectangularRoom): An instance of RectangularRoom to place the
            entity.
        dungeon (GameMap): Instance of GameMap, which holds entities.
        maximum_monters (int): Max number of monsters to place.
    """
    number_of_monsters = random.randint(0, maximum_monsters)
    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(
            [entity.x == x and entity.y == y for entity in dungeon.entities]
        ):
            if random.random() < 0.8:
                entity_factories.orc.spaws(dungeon, x, y)
            else:
                entity_factories.troll.spaws(dungeon, x, y)


def tunel_between(
    start: t.Tuple[int, int],
    end: t.Tuple[int, int],
) -> t.Iterator[t.Tuple[int, int]]:
    """
    This function takes two arguments, both Tuples conssting of two integers.
        It should return an Iterator of a Tuple of two ints. All the tuples
        wil be "x" and "y" coordinates on the map.
    Parameters:
        start (Tuple[int, int]): Starting point of the tunnel.
        end (Tuple[int, int]): Ending point of the tunnel.
    Returns:
        Iterator[Tuple[int, int]]: Return an L-shaped tunnel between these two
            points.
    """
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        # move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_heigth: int,
    max_monster_per_room: int,
    engine: Engine,
) -> GameMap:
    """
    Generate a new dungeon map.
    Parameters:
        max_rooms (int): The maximum number of rooms allowd in the dungeon.
        room_min_size (int): The minimum size of one room.
        room_max_size (int): The maximum size of one room.
        map_width (int): The width of the GameMap to create.
        map_height (int): The heigth of the GameMap to create.
        max_monster_per_room (int): Maximum number of monters that can be
            spawned into a room.
        engine (Engine): The engine this dungeon is related to.
    Returns:
        GameMap:
    """
    player = engine.player
    dungeon = GameMap(engine, map_width, map_heigth, entities=[player])
    rooms: t.List[RectangularRoom] = []

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)
        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for x, y in tunel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_monster_per_room)
        rooms.append(new_room)

    return dungeon
