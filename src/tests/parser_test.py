from parser.Grammar import Grammar
from parser.Tokens import Tokens
from tests.TestErrorListener import TestErrorListener
from tests.util import get_parse_tree

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

        tree = parser.program()  # Program is Entry point
        # Convert the tree to a string and compare it to the expected output
        actual_output = tree.toStringTree(recog=parser).strip()
        return actual_output, error_listener.getErrors()

    def test_basic(self):
        p = Path(__file__).parent / "outputs/full_basic.txt"
        with open(str(p), "r") as expected_file:
            expected_output = expected_file.read().strip()
        actual_output, errors = self.get_output("inputs/full_basic.txt")
        self.assertEqual(expected_output, actual_output)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGameParser('test_basic'))
    return suite


runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())
