import typing as t

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from just_another_rogue.entity import Entity
from just_another_rogue.game_map import GameMap
from just_another_rogue.input_handlers import EventHandler


class Engine:
    """
    Engine class responsibilities is to draw the map and the entities, as well
        as handling the player's input.
    Properties:
        entities (Set[Entity]): Is a set, which behaves kind of like a list
            enforces uniqueness. That is, we can't add an Entity to the set
            twice, where as a list would allow that.
        event_handler (EventHandler): It will handle our events.
        game_map (GameMap): The representation of the map.
        player (Entity): Is the player Entity. We have a separate reference to
            it outside of entities for ease of access. We'll need to access
            player a lot more than a random entity in entities.
    """
    def __init__(
        self,
        entities: t.Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity
    ) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: t.Iterable[t.Any]) -> None:
        """
        Method to handle the events. We pass the events to it so it can iterate
            through them.
        Parameters:
            events (Iterable[Any]): "List" of events.
        """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov()  # Update the FOV before the players next action.

    def update_fov(self) -> None:
        """
        Recumpute the visible area based on the players point of vew.
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8)

        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """
        Render handles drawing our screen. call for the GameMap's render
            method. And then we iterate through the self.entities
            and print them to ther proper locations, then present the context,
            and clear the console.
        Parameters:
            console (Console): A console object containing a grid of characters
                with foreground/background colors.
            context (Context): Context manager for libtcod context objects.
        """
        self.game_map.render(console)

        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
