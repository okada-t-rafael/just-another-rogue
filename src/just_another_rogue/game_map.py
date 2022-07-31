import numpy as np
from tcod.console import Console

from just_another_rogue import tile_types


class GameMap:
    """
    Class GameMap holds information regarding the map size and tiles. Has
        methods to render itself and to evaluate whether a coordinate is within
        its bounds.
    Properties:
        width (int): Width of this map.
        height (int): Height of this map.
        tiles (np.ndarray): 2D array filled with tiles representing the wall.
        visible (np.ndarray): Tiles the player can currently see
        explored (np.ndarray): Tiles the player has seen before
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

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
