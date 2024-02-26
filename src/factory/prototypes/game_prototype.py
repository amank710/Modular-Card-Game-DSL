from src.factory.config import Config
from src.factory.player import Player


class GamePrototype:
    def __init__(self):
        self.config_obj = None

        self.players: dict[str, Player] = {}
        self.current_player_index = 0

    def get_config_object(self) -> Config:
        if self.config_obj is None:
            raise Exception("Config object has not been correctly created!")

        return self.config_obj

    def set_config_object(self, config_obj: Config):
        self.config_obj = config_obj
        
    def set_player_object(self, player: Player):
        self.players[player.get_role()] = player

    def get_player(self):
        player = self.players[list(self.players.keys())[self.current_player_index]]
        self.current_player_index = (self.current_player_index + 1) % len(self.players.keys())
        return player

    def get_all_players(self):
        return [self.players[key] for key in self.players.keys()]

    def add_player(self, player):
        pass
