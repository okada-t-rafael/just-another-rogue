import copy
import tcod

from just_another_rogue import entity_factories
from just_another_rogue.engine import Engine
from just_another_rogue.procgen import generate_dungeon


def main() -> bool:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 50
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monster_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        path="dejavu10x10_gs_tc.png",
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD)

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_heigth=map_height,
        max_monster_per_room=max_monster_per_room,
        engine=engine
    )

    engine.update_fov()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Just Another Rogue",
        vsync=True,
    ) as context:

        root_console = tcod.Console(
            width=screen_width,
            height=screen_height,
            order="F")

        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
