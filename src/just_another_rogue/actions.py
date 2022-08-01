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
    Properties:
        entity (Entity): The object performing the action.
    """
    def __init__(self, entity: Entity) -> None:
        self.entity: Entity = entity

    @property
    def engine(self) -> Engine:
        """
        Returns:
            Engine: Returns the engine this action is related to.
        """
        return self.entity.game_map.engine

    def perform(self) -> None:
        """
        Performs this action with the objects need to determine its scope.
        Note:
            This method must be overriden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    EscapeAction represents the action when the we hit the Esc key (to exit the
        game).
    """
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    """
    Whenever we have an "action" that is related somehow with directions, we'll
        use of the subclasses of ActionWithDirection instead of sublcasses of
        Action to describe it.
    Properties:
        entity (Entity): The object performing the action.
        dx (int): Amount of units to move in the x direciton.
        dy (int): Amount of units to move in the y direciton.
    """
    def __init__(self, entity: Entity, dx: int, dy: int) -> None:
        super().__init__(entity)
        self.dx: int = dx
        self.dy: int = dy

    @property
    def dest_xy(self) -> t.Tuple[int, int]:
        """
        Returns:
            Tuple[int, int]: This action's destination.
        """
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> t.Optional[Entity]:
        """
        Returns:
            Optional[Entity]: Returns the blocking entity at this actions
                destinations.
        """
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)  # noqa: E501

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """
    MeeeAction represents action to describe the player attacking other
        entities.
    """
    def perform(self) -> None:
        """
        Implements  what we'll use to attack.. eventually.
        """
        target: t.Optional[Entity] = self.blocking_entity

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
    def perform(self) -> None:
        """
        Performs this action with the objects need to determine its scope.
            Tries to update the entity position, given the amount of units to
            move the entity in the x and y directions. If the new position is
            out of map bounds or is blocked, the actions "fails", i.e. the
            entity coordinate does not update.
        """
        dest_x: int
        dest_y: int

        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if self.blocking_entity:
            return

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """
    BumpAction determines which one action is appropriate to call (MeleeAction
        or MovementAction) based on whether there is a blocking entity at the
        given destination or not.
    """
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
