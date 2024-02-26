from src.factory.config import Config
from src.factory.config_builder import ConfigBuilder

from src.game.objects.variable import Variable

from src.tests.util import get_ast, get_parse_tree

import unittest


class TestConfigBuilder(unittest.TestCase):
    def test_config_builder_basic(self):
        tree = get_ast(get_parse_tree(file_path="input_config_builder.txt"))
        print('\n')
        print(tree)

        config_builder = ConfigBuilder()
        config_prototype = config_builder.build(root_node=tree)
        config = Config(config_prototype=config_prototype)

        print(config)

        expected_variable_map = dict()
        expected_variable_map["GLOBAL"] = dict()
        expected_variable_map["PLAYER"] = { "score": Variable(name="score"),
                                           "result": Variable(name="result"),
                                           "input": Variable(name="input") }
        expected_variable_map["DEALER"] = { "score": Variable(name="score"),
                                           "result": Variable(name="result"),
                                           "input": Variable(name="input") }


        self.assertEqual(["PLAYER", "DEALER"], config.get_roles())
        self.assertEqual(expected_variable_map, config.get_variables())
        self.assertEqual(52, len(config.cards))
