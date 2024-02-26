from src.parser.Tokens import Tokens
from src.parser.Grammar import Grammar
from src.tests.TestErrorListener import TestErrorListener

from antlr4 import *
from pathlib import Path
import unittest


class TestGameParser(unittest.TestCase):

    def parse_input(self, input_file):
        p = Path(__file__).parent / input_file
        input_stream = FileStream(str(p))
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)

        error_listener = TestErrorListener()
        parser.removeErrorListeners()  # Remove default console error listener
        parser.addErrorListener(error_listener)  # Add custom error listener

        tree = parser.program()  # assuming 'config' is your entry point
        return tree.toStringTree(recog=parser).strip(), error_listener.getErrors()

    def test_complete_configuration(self):
        actual_output, errors = self.parse_input("input_complete_config.txt")
        p = Path(__file__).parent / "test_complete_config.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip()
        self.assertEqual(actual_output, expected_output)
        self.assertEqual(1, len(errors))

    def test_actions_with_missing_details(self):
        _, errors = self.parse_input("input_actions_no_assignment.txt")
        self.assertTrue('mismatched input \';\'' in errors[0] and '{SYSTEM_ACTION, STRING}' in errors[0])

    def test_variable_structure_without_assignments(self):
        _, errors = self.parse_input("input_variable_no_assignment.txt")
        self.assertTrue('mismatched input \';\'' in errors[0] and 'STRING' in errors[0])

    def test_roles_with_invalid_syntax(self):
        _, errors = self.parse_input("input_roles_missing_and.txt")
        self.assertTrue('mismatched input \'DEALER\'' in errors[0] and 'AND' in errors[0])

if __name__ == '__main__':
    unittest.main()
