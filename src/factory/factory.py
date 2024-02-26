from src.factory.config import Config
from src.factory.config_builder import ConfigBuilder
from src.dsl_ast.ast_node import ProgramNode
from src.factory.player import Player
from src.factory.player_builder import PlayerBuilder
from src.factory.prototypes.game_prototype import GamePrototype
from src.game.game import Game


class Factory:
    def __init__(self, ast: ProgramNode) -> None:
        self.tree = ast
        self.game_proto = GamePrototype()
        self.players = []

    def build_game(self, cons_queue=None):
        config = self.build_config()
        # print(config)
        self.build_players(config)
        
        self.players = self.game_proto.get_all_players()

        return Game(self.game_proto)

    def build_config(self):
        config = Config(config_prototype=ConfigBuilder().build(self.tree))
        self.game_proto.set_config_object(config)
        return config

    def build_players(self, config: Config):
        for role in config.get_roles():
            p = Player(prototype=PlayerBuilder(config=config, role=role).build(self.tree))
            self.game_proto.set_player_object(p)

    def get_players(self):
        return self.players
