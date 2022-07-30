class Action:
    """
    Whenever we have an "action", we'll use one of the subclasse of Action to
        describe it. We'll be able to detect which subclass we're using, and
        respond accordingly.
    """
    pass


class EscapeAction(Action):
    """
    EscapeAction represents the action when the we hit the Esc key (to exit the
        game).
    """
    pass


class MovementAction(Action):
    """
    MovementAction represents actions to describe the player moving around.
        More than just knowing that the player is trying to move, MovemntAction
        tell us where the player is trying to move to with the properties dx
        and dy.
    """
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy
