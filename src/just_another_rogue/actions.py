from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from just_another_rogue.engine import Engine
    from just_another_rogue.entity import Entity


class Action:
    """
    Whenever we have an "action", we'll use one of the subclasse of Action to
        describe it. We'll be able to detect which subclass we're using, and
        respond accordingly.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Performs this action with the objects need to determine its scope.
        Parameters:
            engine (Engine): Is the scope this action is being performed in.
            entity (Entity): is the object performing the action.
        Note:
            This method must be overriden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    EscapeAction represents the action when the we hit the Esc key (to exit the
        game).
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    """
    Whenever we have an "action" that is related somehow with directions, we'll
        use of the subclasses of ActionWithDirection instead of sublcasses of
        Action to describe it.
    Properties:
        dx (int): Amount of units to move in the x direciton.
        dy (int): Amount of units to move in the y direciton.
    """
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """
    MeeeAction represents action to describe the player attacking other
        entities.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Implements  what we'll use to attack.. eventually.
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(
            dest_x, dest_y)

        if not target:
            return

        print(f"You kick the {target.name}, much to its annoyance!")


class MovementAction(ActionWithDirection):
    """
    MovementAction represents actions to describe the player moving around.
        More than just knowing that the player is trying to move, MovemntAction
        tell us where the player is trying to move to with the properties dx
        and dy.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Performs this action with the objects need to determine its scope.
            Tries to update the entity position, given the amount of units to
            move the entity in the x and y directions. If the new position is
            out of map bounds or is blocked, the actions "fails", i.e. the
            entity coordinate does not update.
        Parameters:
            engine (Engine): Is the scope this action is being performed in.
            entity (Entity): is the object performing the action.
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination os blocked by a tile
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """
    BumpAction determines which one action is appropriate to call (MeleeAction
        or MovementAction) based on whether there is a blocking entity at the
        given destination or not.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
