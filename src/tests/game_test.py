from parser.Tokens import Tokens
from parser.Grammar import Grammar
from tests.TestErrorListener import TestErrorListener

from antlr4 import *
from pathlib import Path
import unittest


class TestGameParser(unittest.TestCase):
    def get_output(self, filepath):
        # Process the input file and generate the parse tree
        p = Path(__file__).parent / filepath
        input_stream = FileStream(str(p))
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)

        error_listener = TestErrorListener()
        parser.removeErrorListeners()  # Remove default console error listener
        parser.addErrorListener(error_listener)  # Add custom error listener
        parser.reset()

        tree = parser.program()  # Game is Entry point
        # Convert the tree to a string and compare it to the expected output
        actual_output = tree.toStringTree(recog=parser)
        return actual_output.strip(), error_listener.getErrors()

    def test_game(self):
        p = Path(__file__).parent / "outputs/full_game.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip()
        actual_output, errors = self.get_output("inputs/full_game.txt")
        print(actual_output)
        self.assertEqual(actual_output, expected_output)

    def test_missing_game(self):
        _, errors = self.get_output("inputs/missing_game.txt")
        self.assertTrue("mismatched input" in errors[0] and "expecting \'GAME\'" in errors[0])

    def test_func_missing_end(self):
        _, errors = self.get_output("inputs/missing_endFunc.txt")
        self.assertTrue("mismatched input" in errors[0] and "expecting FUNC_END" in errors[0])

    def test_loop_no_conditional(self):
        _, errors = self.get_output("inputs/missing_loop_conditional.txt")
        print(errors)
        self.assertTrue("mismatched input \')\'" in errors[0] and "BOOLEAN, INTEGER, ENTITY_CARD" in errors[0])

    def test_no_statements(self):
        _, errors = self.get_output("inputs/empty_common.txt")
        self.assertTrue("mismatched input" in errors[0] and "expecting {OVERRIDABLE_FUNCTION, ACTION_CALLBACK}" in errors[0])

    # def test_missing_end_nested(self):
    #     _, errors = self.get_output("inputs/missing_end_nested_loop.txt")
    #     self.assertTrue(
    #         any("missing" in e[2] and "LOOP_END" in e[2] for e in errors))

    def test_missing_op_if(self):
        _, errors = self.get_output("inputs/if_missing_op.txt")
        self.assertTrue("mismatched input \')\'" in errors[0] and "BOOLEAN, INTEGER, ENTITY_CARD" in errors[0])

    def test_incorrect_user(self):
        _, errors = self.get_output("inputs/incorrect_user.txt")
        self.assertTrue(
            "mismatched input 'score'" in errors[0])

    def test_func_outside(self):
        _, errors = self.get_output("inputs/func_outside.txt")
        self.assertTrue("mismatched input 'setup' expecting 'RESULT'" in errors[0])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGameParser('test_game'))
    suite.addTest(TestGameParser('test_missing_game'))
    suite.addTest(TestGameParser('test_func_missing_end'))
    suite.addTest(TestGameParser('test_loop_no_conditional'))
    suite.addTest(TestGameParser('test_no_statements'))
    # suite.addTest(TestGameParser('test_missing_end_nested'))
    suite.addTest(TestGameParser('test_missing_op_if'))
    suite.addTest(TestGameParser('test_incorrect_user'))
    suite.addTest(TestGameParser('test_func_outside'))
    return suite


runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())
