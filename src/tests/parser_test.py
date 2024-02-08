from antlr4 import *
from Tokens import Tokens
from Grammar import Grammar
import unittest
from TestErrorListener import TestErrorListener

class TestGameParser(unittest.TestCase):
    def get_output(self, filepath): 
        # Process the input file and generate the parse tree
        input_stream = FileStream(filepath)
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)

        error_listener = TestErrorListener()
        parser.removeErrorListeners()  # Remove default console error listener
        parser.addErrorListener(error_listener)  # Add custom error listener

        tree = parser.game()  # Game is Entry point
        # Convert the tree to a string and compare it to the expected output
        actual_output = tree.toStringTree(recog=parser).strip()
        return actual_output, error_listener.getErrors()
    
    def test_basic(self):
        with open("outputs/full_basic.txt", "r") as expected_file:
            expected_output = expected_file.read().strip()
        actual_output, errors = self.get_output("inputs/full_basic.txt")
        self.assertEqual(actual_output, expected_output)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGameParser('test_basic'))
    return suite

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())