
from antlr4 import *
from pathlib import Path
from src.dsl_ast.variables_checker_visitor import VariablesCheckerVisitor
from src.tests.util import get_ast, get_parse_tree
import unittest
import unittest


class TestGameParser(unittest.TestCase):
    def get_output(self, filepath):
        tree = get_ast(get_parse_tree(file_path=filepath))
        print('\n')
        print(tree)
        checker = VariablesCheckerVisitor()
        return checker.check(tree)

    def test_missing_declaration(self):
        p = Path(__file__).parent / "outputs/missing_declared_variable.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output("inputs/missing_declared_variable.txt")
        print(errors)
        print(expected_output)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_uninitialized_variable(self):
        p = Path(__file__).parent / "outputs/uninitialized_variable.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output("inputs/uninitialized_variable.txt")
        print(errors)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_if_node_uninitialized_variable(self):
        p = Path(__file__).parent / "outputs/if_node_uninitialized_variable.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output("inputs/if_node_uninitialized_variable.txt")
        print(errors)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_multiple_failures(self):
        p = Path(__file__).parent / \
            "outputs/multiple_failures.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output("inputs/multiple_failures.txt")
        print(errors)
        print(expected_output)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_missing_declared_role_in_variables(self):
        p = Path(__file__).parent / \
            "outputs/missing_declared_role_in_variables.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output(
            "inputs/missing_declared_role_in_variables.txt")
        print(errors)
        print(expected_output)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_missing_declared_user_action(self):
        p = Path(__file__).parent / \
            "outputs/undeclared_on_xxx_function.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output(
            "inputs/undeclared_on_xxx_function.txt")
        print(errors)
        print(expected_output)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_undeclared_user_action_waitfor(self):
        p = Path(__file__).parent / \
            "outputs/undeclared_waitfor_action.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip().split('\n')
        errors = self.get_output(
            "inputs/undeclared_waitfor_action.txt")
        print(errors)
        print(expected_output)
        self.assertEqual(len(errors), len(expected_output))
        for i in range(len(errors)):
            self.assertEqual(errors[i], expected_output[i])

    def test_no_error(self):
        errors = self.get_output(
            "input.txt")
        self.assertEqual(len(errors), 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGameParser('test_missing_declaration'))
    suite.addTest(TestGameParser('test_uninitialized_variable'))
    suite.addTest(TestGameParser('test_if_node_uninitialized_variable'))
    suite.addTest(TestGameParser('test_multiple_failures'))
    suite.addTest(TestGameParser('test_missing_declared_role_in_variables'))
    suite.addTest(TestGameParser('test_missing_declared_user_action'))
    suite.addTest(TestGameParser('test_undeclared_user_action_waitfor'))
    return suite


runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())
