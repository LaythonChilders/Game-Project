import json
from object_handler import *


class save_state:
    def __init__(self, game):
        self.game = game
        self.loaded_data = None  # Store the loaded game data

    def get_game_state(self):
        # Extract all necessary data from the game state
        self.npc_list = self.game.object_handler.npc_list  # This is an array of NPC objects
        self.player_health = self.game.player.health
        self.player_pos = self.game.player.map_pos
        self.score = self.game.score_system.current_score
        self.theme = self.game.theme

    def save_game_state(self):
        # Prepare the data for saving
        game_state = {
            "player": {
                "health": self.player_health,
                "position": self.player_pos,
            },
            "score": self.score,
            "theme": self.theme,
            "npcs": [
                {
                    "type": type(npc).__name__,  # Save the NPC class name
                    "position": npc.map_pos,
                    "health": npc.health,
                    "path": npc.path,
                    "scale": npc.scale,
                    "shift": npc.shift,
                    "animation_time": npc.animation_time,
                    "point_value": npc.point_value,
                    "health_value": npc.health_value,
                    "attack_damage": npc.attack_damage,
                }
                for npc in self.npc_list
            ],
        }

        # Write the game state to a JSON file
        try:
            with open("game_state.json", "w") as file:
                json.dump(game_state, file, indent=4)
            print("Game state saved successfully!")
        except IOError as e:
            print(f"Failed to save game state: {e}")

    def load_game_state(self):
        # Read the game state from a JSON file
        try:
            with open("game_state.json", "r") as file:
                self.loaded_data = json.load(file)
            print("Game state loaded successfully!")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to load game state: {e}")
            self.loaded_data = None

    def apply_loaded_game_state(self):
        if not self.loaded_data:
            print("No game state loaded to apply!")
            return

        # Restore player data
        player_data = self.loaded_data.get("player", {})
        self.game.player.health = player_data.get("health", 100)  # Default health if missing
        self.game.player.map_pos = tuple(player_data.get("position", (0, 0)))

        # Restore score and theme
        self.game.score_system.current_score = self.loaded_data.get("score", 0)
        self.game.theme = self.loaded_data.get("theme", "default_theme")

        # Restore NPC data
        npc_data = self.loaded_data.get("npcs", [])
        self.game.object_handler.npc_list = self.create_npcs_from_data(npc_data)

    def create_npcs_from_data(self, npc_data):
        # Generate an array of NPCs based on the saved data
        npc_list = []
        for npc_info in npc_data:
            npc_type = npc_info.get("type", "NPC")  # Fallback to generic NPC if type is missing
            npc_class = globals().get(npc_type, NPC)  # Get the class dynamically
            npc = npc_class(
                self.game,
                path=npc_info.get("path", ""),
                pos=tuple(npc_info.get("position", (0, 0))),
                scale=npc_info.get("scale", 0.6),
                shift=npc_info.get("shift", 0.3),
                animation_time=npc_info.get("animation_time", 180),
                point_value=npc_info.get("point_value", 10),
                health_value=npc_info.get("health_value", 0),
                attack_damage=npc_info.get("attack_damage", 10),
            )
            npc.health = npc_info.get("health", npc.health)  # Set initial health
            npc_list.append(npc)
        return npc_list
