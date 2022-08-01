from __future__ import annotations

import tcod.event
import typing as t

from just_another_rogue.actions import Action, BumpAction, EscapeAction


if t.TYPE_CHECKING:
    from just_another_rogue.engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    EventHandler is a subclass of tcod's EventDispatch class. EventDispatch is
        a class that allow us to send an event to its proper method based on
        what type of event it is.
    Properties:
        engine (Engine): Engine related to this EventHandler.
    """
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        """
        Method to handle the events. Iterate through the events and perform the
            action if any. After that calls for the engine to handle ememies'
            turns and handle the fov.
        """
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> t.Optional[Action]:
        """
        This method overrides the EventDispatch:ev_quit. It is called when a
            "quit" event is received, which happens when we click the "X" in
            the windows of the program. In that case, we want to quit the
            program, so we raise SystemExit() to do so.
        """
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> t.Optional[Action]:
        """
        This method will receive key press events, and return either an Action
            subclass, or None, if no valid key was pressed.
        """
        key = event.sym
        player = self.engine.player
        actions: t.Dict[int, Action] = {
            tcod.event.K_UP: BumpAction(player, dx=0, dy=-1),
            tcod.event.K_DOWN: BumpAction(player, dx=0, dy=1),
            tcod.event.K_LEFT: BumpAction(player, dx=-1, dy=0),
            tcod.event.K_RIGHT: BumpAction(player, dx=1, dy=0),
            tcod.event.K_ESCAPE: EscapeAction(player)
        }
        return actions.get(key, EscapeAction(player))
