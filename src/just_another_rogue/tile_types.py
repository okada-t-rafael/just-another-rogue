import numpy as np  # type: ignore
import typing as t


"""
Tile graphics structure type compatible with Console.tiles_rgb.
ch (np.int32): The character, represented in integer format. We'll
    translate it from the integer into Unicode.
fg (3B): The foreground color. "3B" means 3 unsigned bytes, which can be
    used for RGB color codes.
bg (3B): The background color Similar to fg.
"""
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

"""
Tile struct used for statically defined tile data.
walkable (np.bool): A boolean that describes if the player can walk across
    this tile.
transparent (np.bool): A boolean that describes if this tile does or not
    block the field of view.
dark (graphic_dt): This uses our previously defined dtype, which holds the
    character to print, the foregroun color, and the background color. Why
    is it called dark? Because later on, we'll want to differentiate
    between tiles that are and aren't in the field of view. dark will
    represent tiles that are not in the current field of view.
light (graphic_dt): Light will hod the information about what our tile looks
    like when it's in the field of view.
"""
tile_dt = np.dtype(
    [
        ("walkable", np.bool8),
        ("transparent", np.bool8),
        ("dark", graphic_dt),
        ("light", graphic_dt),
    ]
)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: t.Tuple[int, t.Tuple[int, int, int], t.Tuple[int, int, int]],
    light: t.Tuple[int, t.Tuple[int, int, int], t.Tuple[int, int, int]],
) -> np.ndarray:
    """
    Helper function for defining individual tiles types.
    Parameters:
        walkable (bool): True if this tile can be walked over.
        tranparent (bool): True if this tile doesn't block FOV.
        dark (Tuple[int, Tuple[int...], Tuple[int...]]): Graphics for when this
            tile is not in FOV. See graphic_dt.
        light (Tuple[int, Tuple[int...], Tuple[int...]]): Graphics for when the
            tile is in FOV.
    Note:
        *, Enforce the use of keywords, so that parameter order doesn't matter.
    """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


"""
SHROUD represents unexplroed, unseed tiles
"""
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


"""
Tile representing the floor.
"""
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50))
)

"""
Tile representing the wall.
"""
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50))
)
