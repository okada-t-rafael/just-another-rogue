import tcod.event
import typing as t

from just_another_rogue.actions import Action, BumpAction, EscapeAction


class EventHandler(tcod.event.EventDispatch[Action]):
    """
    EventHandler is a subclass of tcod's EventDispatch class. EventDispatch is
        a class that allow us to send an event to its proper method based on
        what type of event it is.
    """

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
        actions = {
            tcod.event.K_UP: BumpAction(dx=0, dy=-1),
            tcod.event.K_DOWN: BumpAction(dx=0, dy=1),
            tcod.event.K_LEFT: BumpAction(dx=-1, dy=0),
            tcod.event.K_RIGHT: BumpAction(dx=1, dy=0),
        }
        return actions.get(key, EscapeAction())
