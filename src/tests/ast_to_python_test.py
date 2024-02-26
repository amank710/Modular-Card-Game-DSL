from src.factory.function_context.expressions.binary_expression import BinaryExpression
from src.factory.function_context.expressions.constant_expression import ConstantExpression
from src.factory.config import Config
from src.factory.config_builder import ConfigBuilder
from src.factory.factory import Factory
from src.factory.player import Player
from src.factory.player_builder import PlayerBuilder
from src.factory.prototypes.game_prototype import GamePrototype
from src.game.objects.game_effect import PlayerControlStatus
from src.game.objects.variable import Variable
from src.factory.prototypes.player_prototype import PlayerPrototype
from src.game.game import Game
from src.tests.util import get_ast, get_parse_tree
from src.factory.types.callback_type import CallbackType

from src.factory.types.callback_type import CallbackType


import logging
import unittest

logging.getLogger().setLevel(logging.DEBUG)

class TestAstToPython(unittest.TestCase):
    # This test is to check if the player is able to get updated when the game is played
    def test_game_player(self):
        logging.getLogger().setLevel(logging.DEBUG)
        # Create the AST
        tree = get_ast(get_parse_tree(file_path="input.txt"))
        print(tree)
        
        f = Factory(ast=tree)
        game = f.build_game()
        print("before")

        print(game.get_players_data()[0])

        print(f.get_players())
        role1 = f.get_players()[1]
        role2 = f.get_players()[0]
        role1.setup()
        role2.setup()

        print("after")
        print(game.get_players_data()[0])


        # Comparing the callback function to a mock creation of HIT based on MVP
        callback = role1.get_callback()['HIT']
        callback_string = callback.__repr__()
        mock_hit_string = "0: PLAYER.score = ARITHMETIC (VAR: PLAYER.score + VAR: PLAYER.card)\n"
        assert mock_hit_string == callback_string

        callback_dealer = role2.get_callback()['HIT']
        callback_string_dealer = callback_dealer.__repr__()
        mock_hit_string_dealer = "0: DEALER.score = ARITHMETIC (VAR: DEALER.score + VAR: DEALER.card)\n"
        assert mock_hit_string_dealer == callback_string_dealer


        variable = Variable(name='card')
        variable.set_value(1)
        role1.update_local_vars('PLAYER', 'card', variable)

        variable2 = Variable(name='card')
        variable2.set_value(12)
        role2.update_local_vars('DEALER', 'card', variable2)

        callback.execute()
        callback_dealer.execute()
        print(game.get_players_data()[0])

        # Comparing score after arithmetic to mock score for MVP
        mock_player_score = Variable("score")
        mock_player_score.set_value(1) # Assume PLAYER has score = 1
        assert game.get_players_data()[0]['PLAYER']['score'] == mock_player_score

        mock_dealer_score = Variable("score")
        mock_dealer_score.set_value(12)
        assert game.get_players_data()[0]['DEALER']['score'] == mock_dealer_score

        callback = role1.get_callback()[CallbackType.ON_TURN]
        output = callback.execute()
        logging.debug("\nonturn repr: " + str(callback))
        logging.debug("---on_turn waitFor()---: \n" + str(output))
        actions = output.get_actions()
        for act in actions.keys():
            if act.get_user_action() == "HIT":
                actions[act] = True
        role1.set_user_actions(action_map=actions)

        output = callback.execute()
        logging.debug("---on_turn_ waitForAssignment---: \n" + str(output))
        print(role1.get_local_vars())
        actions = output.get_actions()
        for act in actions.keys():
            if act.get_user_action() == "HIT":
                actions[act] = True
        role1.set_user_actions(action_map=actions)

        output = callback.execute()
        logging.debug("---on_turn loop waitFor---: \n" + str(output))
        print(role1.get_local_vars())
        assert role1.get_local_vars()["PLAYER"]["action"].get_value() == "HIT"

        actions = output.get_actions()
        for act in actions.keys():
            if act.get_user_action() == "STAY":
                actions[act] = True
        role1.set_user_actions(action_map=actions)
        logging.debug("---on_turn loop waitFor now STAY---: \n" + str(output))
        output = callback.execute()
        print(role1.get_local_vars())
        assert role1.get_local_vars()["PLAYER"]["action"].get_value() == "STAY"
        assert output.get_player_control_status() == PlayerControlStatus.TURN_DONE



    def test_non_zero_setup(self):
        logging.getLogger().setLevel(logging.DEBUG)
        # Create the AST
        tree = get_ast(get_parse_tree(file_path="inputs/non_zero_setup.txt"))
        print(tree)

        f = Factory(ast=tree)
        game = f.build_game()
        print("before")

        print(game.get_players_data()[0])

        print(f.get_players())
        role1 = f.get_players()[0]
        role2 = f.get_players()[1]
        role1.setup()
        role2.setup()

        print("after")
        print(game.get_players_data()[0])


        # Comparing the callback function to a mock creation of HIT based on MVP
        callback = role1.get_callback()['HIT']
        callback_string = callback.__repr__()
        mock_hit_string = "0: PLAYER.score = ARITHMETIC (VAR: PLAYER.score + VAR: PLAYER.card)\n"
        assert mock_hit_string == callback_string

        callback_dealer = role2.get_callback()['HIT']
        callback_string_dealer = callback_dealer.__repr__()
        mock_hit_string_dealer = "0: DEALER.score = ARITHMETIC (VAR: DEALER.score + VAR: DEALER.card)\n"
        assert mock_hit_string_dealer == callback_string_dealer


        variable = Variable(name='card')
        variable.set_value(1)
        role1.update_local_vars('PLAYER', 'card', variable)

        variable2 = Variable(name='card')
        variable2.set_value(12)
        role2.update_local_vars('DEALER', 'card', variable2)

        callback.execute()
        callback_dealer.execute()
        print(game.get_players_data()[0])

        # Comparing score after arithmetic to mock score for MVP
        mock_player_card = Variable("card")
        mock_player_card.set_value(1) # Assume PLAYER has score = 1

        mock_player_score = Variable("score")
        mock_player_score.set_value(3) # Assume PLAYER has score = 1

        assert game.get_players_data()[0]['PLAYER']['card'] == mock_player_card
        assert game.get_players_data()[0]['PLAYER']['score'] == mock_player_score

        mock_dealer_card = Variable("card")
        mock_dealer_card.set_value(12)

        mock_dealer_score = Variable("score")
        mock_dealer_score.set_value(17)
        assert game.get_players_data()[0]['DEALER']['card'] == mock_dealer_card
        assert game.get_players_data()[0]['DEALER']['score'] == mock_dealer_score




        # print(callback.get_name())
        # print(callback.get_statements())
        #
        # mock_player_result = Variable("result")
        # mock_player_result.set_value("WIN")
        # print("Mock result ", mock_player_result)
        # print("Getting result ", game.get_players_data()[0]['PLAYER']['result'])
        # assert game.get_players_data()[0]['PLAYER']['result'] == mock_player_result
        #
        # mock_dealer_result = Variable("result")
        # mock_dealer_result.set_value("LOST")
        # assert game.get_players_data()[0]['DEALER']['result'] == mock_dealer_result


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAstToPython('test_game_player'))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
