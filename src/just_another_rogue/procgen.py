from __future__ import annotations

import random
import tcod
import typing as t

from just_another_rogue import tile_types
from just_another_rogue.entity import Entity
from just_another_rogue.game_map import GameMap


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


def generate_dungeon_old(map_width: int, map_heigth: int) -> GameMap:
    dungeon = GameMap(map_width, map_heigth)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    for x, y in tunel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_heigth: int,
    player: Entity,
) -> GameMap:
    """
    Generate a new dungeon map.
    Parameters:
        max_rooms (int): The maximum number of rooms allowd in the dungeon.
        room_min_size (int): The minimum size of one room.
        room_max_size (int): The maximum size of one room.
        map_width (int): The width of the GameMap to create.
        map_height (int): The heigth of the GameMap to create.
        player (Player): The player Entity. We need this to know where to place
            the player.
    Returns:
        GameMap:
    """
    dungeon = GameMap(map_width, map_heigth)
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
            player.x, player.y = new_room.center
        else:
            for x, y in tunel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon
