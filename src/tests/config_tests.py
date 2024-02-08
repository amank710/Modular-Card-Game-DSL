import unittest
from antlr4 import *
from Tokens import Tokens
from Grammar import Grammar
from src.tests.TestErrorListener import TestErrorListener


class TestGameParser(unittest.TestCase):

    def parse_input(self, input_file):
        input_stream = FileStream(input_file)
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)

        error_listener = TestErrorListener()
        parser.removeErrorListeners()  # Remove default console error listener
        parser.addErrorListener(error_listener)  # Add custom error listener

        tree = parser.config()  # assuming 'config' is your entry point
        return tree.toStringTree(recog=parser).strip(), error_listener.getErrors()

    def test_complete_configuration(self):
        actual_output, errors = self.parse_input("input_complete_config.txt")
        print(actual_output)
        print(errors)
        with open("test_complete_config.txt", "r") as expected_file:
            expected_output = expected_file.read().strip()
        self.assertEqual(actual_output, expected_output)

    def test_missing_configuration_end(self):
        _, errors = self.parse_input("input_missing_config_end.txt")
        print(errors)
        self.assertTrue(any('expecting' in e[2] and 'END CONFIGURATION' in e[2] for e in errors))

    def test_incomplete_card_value_override(self):
        _, errors = self.parse_input("input_incomplete_override.txt")
        print(errors)
        self.assertTrue(any('missing' in e[2] and ';' in e[2] for e in errors))


    def test_actions_with_missing_details(self):
        _, errors = self.parse_input("input_actions_no_assignment.txt")
        print(errors)
        self.assertTrue(any('missing' in e[2] and '{SYSTEM_ACTION, USER_ACTION}' in e[2] for e in errors))

    def test_variable_structure_without_assignments(self):
        _, errors = self.parse_input("input_variable_no_assignment.txt")
        print(errors)
        self.assertTrue(any('expecting' in e[2] and '{BOOLEAN, INTEGER, STRING}' in e[2] for e in errors))

    def test_roles_with_invalid_syntax(self):
        _, errors = self.parse_input("input_roles_missing_and.txt")
        print(errors)
        self.assertTrue(any('expecting' in e[2] and 'AND' in e[2] for e in errors))

# More test methods can be added here...

if __name__ == '__main__':
    unittest.main()
