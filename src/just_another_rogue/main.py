import tcod

from just_another_rogue.engine import Engine
from just_another_rogue.entity import Entity
from just_another_rogue.input_handlers import EventHandler
from just_another_rogue.procgen import generate_dungeon


def main() -> bool:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    event_handler = EventHandler()

    tileset = tcod.tileset.load_tilesheet(
        path="dejavu10x10_gs_tc.png",
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD)

    player = Entity(
        x=int(screen_width / 2),
        y=int(screen_height / 2),
        char="@",
        color=(255, 255, 255))

    npc = Entity(
        x=int(screen_width / 2),
        y=int(screen_height / 2 - 5),
        char="@",
        color=(255, 255, 0))

    entities = {npc, player}
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_heigth=map_height,
        player=player
    )

    engine = Engine(entities, event_handler, game_map, player)

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
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
