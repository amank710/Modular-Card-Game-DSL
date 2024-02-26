from factory.function_context.expressions.binary_expression import BinaryExpression
from factory.function_context.expressions.constant_expression import ConstantExpression
from src.factory.config import Config
from src.factory.config_builder import ConfigBuilder
from src.factory.factory import Factory
from src.factory.player import Player
from src.factory.player_builder import PlayerBuilder
from src.factory.prototypes.game_prototype import GamePrototype
from src.game.objects.variable import Variable
from src.factory.prototypes.player_prototype import PlayerPrototype
from src.game.game import Game
from src.tests.util import get_ast, get_parse_tree
from src.factory.types.callback_type import CallbackType

from src.factory.types.callback_type import CallbackType


import logging
import unittest

class TestIf(unittest.TestCase):

    # This test is to check if the player is able to get updated when the game is played
    def test_basic_if(self):
        logging.getLogger().setLevel(logging.DEBUG)
        # Create the AST
        tree = get_ast(get_parse_tree(file_path="inputs/basic_if.txt"))
        print(tree)

        f = Factory(ast=tree)
        game = f.build_game()
        print("before")
        print(game.get_players_data()[0])

        role1 = f.get_players()['PLAYER']
        role2 = f.get_players()['DEALER']
        role1.setup()
        role2.setup()

        callback = role1.get_callback()['HIT']
        callback_dealer = role2.get_callback()['HIT']

        variable = Variable(name='card')
        variable.set_value(4)
        role1.update_local_vars('PLAYER', 'card', variable)

        variable2 = Variable(name='card')
        variable2.set_value(4)
        role2.update_local_vars('DEALER', 'card', variable2)


        callback.execute()
        callback_dealer.execute()

        mock_player_score = Variable("score")
        mock_player_score.set_value(4)
        assert game.get_players_data()[0]['PLAYER']['score'] == mock_player_score

        mock_dealer_score = Variable("score")
        mock_dealer_score.set_value(14)
        assert game.get_players_data()[0]['DEALER']['score'] == mock_dealer_score


        print("after")
        print(game.get_players_data()[0])