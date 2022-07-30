import typing as t


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
    """
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: t.Tuple[int, int, int]
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        """
        Method move. Move the entity by a given amount.
        Params:
            dx (int): Amount of units to move in the x direciton.
            dy (int): Amount of units to move in the y direciton.
        """
        self.x += dx
        self.y += dy
