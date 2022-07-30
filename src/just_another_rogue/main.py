import tcod

from just_another_rogue.actions import EscapeAction, MovementAction
from just_another_rogue.input_handlers import EventHandler


def main() -> bool:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    event_handler = EventHandler()

    tileset = tcod.tileset.load_tilesheet(
        path="dejavu10x10_gs_tc.png",
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD)

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
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)
            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
