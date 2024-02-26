from src.game.objects.game_action import GameAction
from src.game.objects.game_effect import GameEffect
from src.factory.config import Config
from src.factory.config_builder import ConfigBuilder
from src.factory.player import Player
from src.factory.player_builder import PlayerBuilder
from src.factory.prototypes.game_prototype import GamePrototype
from src.factory.prototypes.player_prototype import PlayerPrototype
from src.game.game import Game
from src.tests.util import get_ast, get_parse_tree
from src.factory.types.callback_type import CallbackType

from src.factory.types.callback_type import CallbackType


import logging
import unittest

class TestPlayerBuilder(unittest.TestCase):
    def test_player_builder_basic(self):
        logging.getLogger().setLevel(logging.DEBUG)
        
        tree = get_ast(get_parse_tree(file_path="input.txt"))
        # print(tree)
        # print(tree)

        config: Config = Config(ConfigBuilder().build(root_node=tree))

        # dealer_proto = PlayerBuilder(config=config, role="DEALER").build(root_node=tree)
        # dealer = Player(prototype=dealer_proto)
        # dealer_proto = PlayerBuilder(config=config, role="DEALER").build(root_node=tree)
        # dealer = Player(prototype=dealer_proto)

        # print(dealer)
        # print(dealer)

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        player_proto = PlayerBuilder(config=config, role="PLAYER").build(root_node=tree)
        player = Player(prototype=player_proto)
        game_proto = GamePrototype()
        game_proto.set_config_object(config)
        game_proto.set_player_object(player)
        game_effect = GameEffect()
        game_effect.append_game_action(GameAction("HIT"))
        game_effect.append_game_action(GameAction("STAY"))
        game_effect.append_game_action(GameAction("SHOW"))
        game = Game(game_proto, game_effect, game_effect)
        game_effect.append_game_action(player.setup())
        game.turn1()
        assert player.get_local_vars()['PLAYER']['score'].get_value() == 21
        
        
        
        #MCU build
        #Factory buildgame
        #build_config and build_game
        #
