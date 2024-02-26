from src.factory.prototypes.config_prototype import ConfigPrototype
from src.dsl_ast.variables_checker_visitor import VariablesCheckerVisitor
from src.tests.util import get_ast, get_parse_tree
import unittest


class TestConfigBuilder(unittest.TestCase):
    def test_config_builder_basic(self):
        tree = get_ast(get_parse_tree(file_path="input_config_builder.txt"))
        print('\n')
        checker = VariablesCheckerVisitor()
        print(tree)
        # errors = checker.check(tree)
        # if len(errors) == 0:
        #     print("No errors")
        # for error in errors:
        #     print(error)
