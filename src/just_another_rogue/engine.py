from __future__ import annotations

import typing as t
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from just_another_rogue.input_handlers import EventHandler

if t.TYPE_CHECKING:
    from just_another_rogue.entity import Entity
    from just_another_rogue.game_map import GameMap


class Engine:
    """
    Engine class responsibilities is to draw the map, as well as handling the
        player's input.
    Properties:
        player (Entity): Is the player Entity. We have a separate reference to
            it outside of entities for ease of access. We'll need to access
            player a lot more than a random entity in entities.
        event_handler (EventHandler): It will handle our events.
        game_map (GameMap): The representation of the map.
    """
    def __init__(self, player: Entity) -> None:
        self.player = player
        self.event_handler = EventHandler(self)
        self.game_map: GameMap

    def handle_enemy_turns(self) -> None:
        """
        This function loops through each entity (minus the player) and prints
            out a message for them. TODO: Replacee this with some code that
            will allow those entities to take real turns.
        """
        for entity in self.game_map.entities - {self.player}:
            print(
                f"The {entity.name} wonders when "
                "it will get to take a real turn.")

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
        context.present(console)
        console.clear()
